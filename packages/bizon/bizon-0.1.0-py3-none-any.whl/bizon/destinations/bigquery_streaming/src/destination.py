import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Type

import polars as pl
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, bigquery_storage_v1
from google.cloud.bigquery import DatasetReference, TimePartitioning
from google.cloud.bigquery_storage_v1.types import (
    AppendRowsRequest,
    ProtoRows,
    ProtoSchema,
)
from google.protobuf.message import Message

from bizon.common.models import SyncMetadata
from bizon.destinations.config import NormalizationType
from bizon.destinations.destination import AbstractDestination
from bizon.engine.backend.backend import AbstractBackend

from .config import BigQueryStreamingConfigDetails
from .proto_utils import get_proto_schema_and_class


class BigQueryStreamingDestination(AbstractDestination):

    def __init__(self, sync_metadata: SyncMetadata, config: BigQueryStreamingConfigDetails, backend: AbstractBackend):
        super().__init__(sync_metadata, config, backend)
        self.config: BigQueryStreamingConfigDetails = config

        if config.authentication and config.authentication.service_account_key:
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                temp.write(config.authentication.service_account_key.encode())
                temp_file_path = temp.name
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

        self.project_id = config.project_id
        self.bq_client = bigquery.Client(project=self.project_id)
        self.bq_storage_client = bigquery_storage_v1.BigQueryWriteClient()
        self.dataset_id = config.dataset_id
        self.dataset_location = config.dataset_location
        self.bq_max_rows_per_request = config.bq_max_rows_per_request

    @property
    def table_id(self) -> str:
        tabled_id = self.config.table_id or f"{self.sync_metadata.source_name}_{self.sync_metadata.stream_name}"
        return f"{self.project_id}.{self.dataset_id}.{tabled_id}"

    def get_bigquery_schema(self) -> List[bigquery.SchemaField]:

        # we keep raw data in the column source_data
        if self.config.normalization.type == NormalizationType.NONE:
            return [
                bigquery.SchemaField("_source_record_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("_source_timestamp", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("_source_data", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("_bizon_extracted_at", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField(
                    "_bizon_loaded_at", "TIMESTAMP", mode="REQUIRED", default_value_expression="CURRENT_TIMESTAMP()"
                ),
                bigquery.SchemaField("_bizon_id", "STRING", mode="REQUIRED"),
            ]

        raise NotImplementedError(f"Normalization type {self.config.normalization.type} is not supported")

    def check_connection(self) -> bool:
        dataset_ref = DatasetReference(self.project_id, self.dataset_id)

        try:
            self.bq_client.get_dataset(dataset_ref)
        except NotFound:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = self.dataset_location
            dataset = self.bq_client.create_dataset(dataset)
        return True

    def append_rows_to_stream(
        self,
        write_client: bigquery_storage_v1.BigQueryWriteClient,
        stream_name: str,
        proto_schema: ProtoSchema,
        serialized_rows: List[bytes],
    ):
        request = AppendRowsRequest(
            write_stream=stream_name,
            proto_rows=AppendRowsRequest.ProtoData(
                rows=ProtoRows(serialized_rows=serialized_rows),
                writer_schema=proto_schema,
            ),
        )
        response = write_client.append_rows(iter([request]))
        return response.code().name

    @staticmethod
    def to_protobuf_serialization(TableRowClass: Type[Message], row: dict) -> bytes:
        """Convert a row to a protobuf serialization"""
        record = TableRowClass()
        record._bizon_id = row["bizon_id"]
        record._bizon_extracted_at = row["bizon_extracted_at"].strftime("%Y-%m-%d %H:%M:%S.%f")
        record._bizon_loaded_at = row["bizon_loaded_at"].strftime("%Y-%m-%d %H:%M:%S.%f")
        record._source_record_id = row["source_record_id"]
        record._source_timestamp = row["source_timestamp"].strftime("%Y-%m-%d %H:%M:%S.%f")
        record._source_data = row["source_data"]
        return record.SerializeToString()

    def load_to_bigquery_via_streaming(self, df_destination_records: pl.DataFrame) -> str:
        # TODO: for now no clustering keys
        clustering_keys = []

        # Create table if it doesnt exist
        schema = self.get_bigquery_schema()
        table = bigquery.Table(self.table_id, schema=schema)
        time_partitioning = TimePartitioning(field="_bizon_loaded_at", type_=self.config.time_partitioning)
        table.time_partitioning = time_partitioning

        table = self.bq_client.create_table(table, exists_ok=True)

        # Create the stream
        write_client = self.bq_storage_client
        tabled_id = self.config.table_id or f"{self.sync_metadata.source_name}_{self.sync_metadata.stream_name}"
        parent = write_client.table_path(self.project_id, self.dataset_id, tabled_id)
        stream_name = f"{parent}/_default"

        # Generating the protocol buffer representation of the message descriptor.
        proto_schema, TableRow = get_proto_schema_and_class(clustering_keys)

        serialized_rows = [
            self.to_protobuf_serialization(TableRowClass=TableRow, row=row)
            for row in df_destination_records.iter_rows(named=True)
        ]

        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.append_rows_to_stream, write_client, stream_name, proto_schema, batch_rows)
                for batch_rows in self.batch(serialized_rows)
            ]
            for future in futures:
                results.append(future.result())

        assert all([r == "OK" for r in results]) is True, "Failed to append rows to stream"

    def write_records(self, df_destination_records: pl.DataFrame) -> Tuple[bool, str]:
        self.load_to_bigquery_via_streaming(df_destination_records=df_destination_records)
        return True, ""

    def batch(self, iterable):
        """
        Yield successive batches of size `batch_size` from `iterable`.
        """

        for i in range(0, len(iterable), self.bq_max_rows_per_request):
            yield iterable[i : i + self.bq_max_rows_per_request]  # noqa
