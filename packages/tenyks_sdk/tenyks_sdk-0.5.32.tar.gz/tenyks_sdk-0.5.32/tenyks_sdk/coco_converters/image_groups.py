from dataclasses import dataclass
from io import BytesIO
from typing import List, Optional

from fastclasses_json import dataclass_json


@dataclass_json
@dataclass
class Image:
    file_name: str
    subset_id: str


@dataclass_json
@dataclass
class Subset:
    id: str
    name: str
    description: str


@dataclass_json
@dataclass
class ImageGroups:
    images: Optional[List[Image]] = None
    subsets: Optional[List[Subset]] = None

    def export(self, **kwargs):
        return self.to_json(**kwargs)

    @classmethod
    def load(cls, stream: BytesIO):
        image_groups = cls.from_json(stream.read())

        return image_groups
