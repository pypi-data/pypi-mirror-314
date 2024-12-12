import json
import os
import re
import unicodedata
from io import BytesIO
from typing import List

import pyarrow as pa
from werkzeug.datastructures import FileStorage

from tenyks_sdk.file_providers.file_resource_provider_factory import (
    FileResourceProviderFactory,
)


class JsonArrowConverter:
    """
    Expected format:
    {
        "image_embeddings": [
            {
                "file_name": str,
                "embeddings": List[float]
            }
        ]
    }
    """

    def convert_cloud_embedding(
        self,
        input_filename: str,
        input_storage_location: dict,
        output_filename: str,
        output_storage_location: dict,
        embedding_type_key: str = "image_embeddings",
        file_name_key: str = "file_name",
        embedding_key: str = "embeddings",
    ):
        embedding_data = self._read_embedding_json_from_cloud(
            input_filename, input_storage_location, embedding_type_key
        )

        arrow_batch = self._convert_embedding_data_to_pyarrow_batch(
            embedding_data, file_name_key, embedding_key
        )

        self._save_table_to_cloud_arrow(
            output_filename, output_storage_location, arrow_batch
        )

    def convert_local_embedding(
        self,
        input_filename: str,
        input_filepath: str,
        output_filename: str,
        output_filepath: str,
        embedding_type_key: str = "image_embeddings",
        file_name_key: str = "file_name",
        embedding_key: str = "embeddings",
    ):
        embedding_data = self._read_embedding_json_from_local(
            input_filename, input_filepath, embedding_type_key
        )

        arrow_batch = self._convert_embedding_data_to_pyarrow_batch(
            embedding_data, file_name_key, embedding_key
        )

        self._save_table_to_local_arrow(output_filename, output_filepath, arrow_batch)
    
    def convert_local_to_cloud_embedding(
        self,
        input_filename: str,
        input_filepath: str,
        output_filename: str,
        output_storage_location: dict,
        embedding_type_key: str = "image_embeddings",
        file_name_key: str = "file_name",
        embedding_key: str = "embeddings",
    ):
        embedding_data = self._read_embedding_json_from_local(
            input_filename, input_filepath, embedding_type_key
        )

        arrow_batch = self._convert_embedding_data_to_pyarrow_batch(
            embedding_data, file_name_key, embedding_key
        )

        self._save_table_to_cloud_arrow(
            output_filename, output_storage_location, arrow_batch
        )

    def _convert_embedding_data_to_pyarrow_batch(
        self, embedding_data: List[dict], file_name_key: str, embedding_key: str
    ):

        embedding_storage_schema = pa.schema(
            [
                ("bbox_id", pa.binary()),
                (
                    "embedding",
                    pa.list_(pa.float32()),
                ),
            ]
        )

        identifiers = []
        vectors = []
        for vector_entry in embedding_data:
            identifiers.append(
                self._convert_filename_to_key(vector_entry[file_name_key]).encode(
                    "utf-8"
                )
            )
            vectors.append(vector_entry[embedding_key])
        data = [pa.array(identifiers), pa.array(vectors)]
        record_batch = pa.RecordBatch.from_arrays(data, schema=embedding_storage_schema)

        return record_batch

    @staticmethod
    def _read_embedding_json_from_local(
        filename: str, filepath: str, embedding_type_key: str
    ):
        if ".json" not in filename:
            filename = filename + ".json"

        with open(os.path.join(filepath, filename), "r") as file:
            embedding_data = json.load(file)

        return embedding_data[embedding_type_key]

    @staticmethod
    def _read_embedding_json_from_cloud(
        filename: str, storage_location: dict, key: str
    ):
        storage_provider = FileResourceProviderFactory.create_resource_provider(
            storage_location
        )
        if ".json" not in filename:
            filename = filename + ".json"

        embedding_data = json.loads(storage_provider.get_file(filename).read().decode())

        return embedding_data[key]

    @staticmethod
    def _save_table_to_local_arrow(filename: str, filepath: str, batch: pa.RecordBatch):
        if ".arrow" not in filename:
            filename = filename + ".arrow"
        with pa.ipc.RecordBatchFileWriter(
            os.path.join(filepath, filename), batch.schema
        ) as writer:
            writer.write_batch(batch)

    @staticmethod
    def _save_table_to_cloud_arrow(
        filename: str,
        storage_location: dict,
        batch: pa.RecordBatch,
    ):
        storage_provider = FileResourceProviderFactory.create_resource_provider(
            storage_location
        )

        byte_object = BytesIO()

        with pa.ipc.new_file(byte_object, batch.schema) as writer:
            writer.write_batch(batch)
        if ".arrow" not in filename:
            filename = filename + ".arrow"

        field_storage_object = FileStorage(byte_object, filename=filename)
        storage_provider.save_file(field_storage_object, filename)

    @staticmethod
    def _convert_filename_to_key(filename: str) -> str:
        FILENAME_ASCII_STRIP_RE = re.compile(r"[^A-Za-z0-9_.-]")
        filename = unicodedata.normalize("NFKD", filename)
        filename = filename.encode("ascii", "ignore").decode("ascii")

        for sep in os.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, " ")
        filename = str(
            FILENAME_ASCII_STRIP_RE.sub("", "_".join(filename.split()))
        ).strip("._")

        name, extension = os.path.splitext(filename)

        return name
