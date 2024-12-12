from io import BytesIO
from typing import Any, Dict, List

import pyarrow as pa
from tenyks_sdk.file_providers.single_file_provider_factory import (
    SingleFileProviderFactory,
)
from werkzeug.datastructures import FileStorage


class ArrowFileStorage:
    def __init__(
        self,
        data: List[Any],
        schema: pa.schema,
        filename: str,
        arrow_file_location: Dict[str, object],
    ):
        self.data = data
        self.schema = schema
        self.filename = filename
        self.arrow_file_location = arrow_file_location

    def save_data_to_file(self):
        data = zip(*self.data)
        data = [pa.array(x) for x in data]

        if len(data) == 0:
            data = [pa.array([]) for _ in self.schema.names]

        record_batch = pa.RecordBatch.from_arrays(data, self.schema)

        byte_object = BytesIO()

        with pa.ipc.new_file(byte_object, self.schema) as writer:
            writer.write_batch(record_batch)

        file_storage = FileStorage(byte_object, filename=self.filename + ".arrow")

        object_embedding_cache_file_provider = (
            SingleFileProviderFactory.create_file_provider_from_location(
                self.arrow_file_location
            )
        )

        object_embedding_cache_file_provider.save_file(file_storage)
