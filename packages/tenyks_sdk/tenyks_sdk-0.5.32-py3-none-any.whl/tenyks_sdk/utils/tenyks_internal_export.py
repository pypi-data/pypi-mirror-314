from dataclasses import dataclass, field
from typing import List, Optional

from fastclasses_json import dataclass_json


@dataclass_json
@dataclass
class TenyksAnnotation:
    bbox_id: str
    category_id: Optional[str] = field(default=None)
    category_name: Optional[str] = field(default=None)
    coordinates: List[float] = field(default_factory=list)
    segmentation: List[List[float]] = field(default_factory=list)


@dataclass_json
@dataclass
class TenyksBoundingBox:
    id: Optional[str] = field(default=None)
    category_id: Optional[str] = field(default=None)
    score: Optional[float] = field(default=None)
    coordinates: List[float] = field(default_factory=list)
    segmentation: List[List[float]] = field(default_factory=list)


@dataclass_json
@dataclass
class TenyksBoundingBoxMatch:
    iou: float
    failure_type: str
    annotation: TenyksBoundingBox = field(default=None)
    prediction: TenyksBoundingBox = field(default=None)
    image_key: str = field(default=None)


@dataclass_json
@dataclass
class TenyksImage:
    image_key: str
    image_filename: Optional[str] = field(default=None)
    width: Optional[int] = field(default=None)
    height: Optional[int] = field(default=None)
    annotations: List[TenyksAnnotation] = field(default_factory=list)
    bounding_box_matches: List[TenyksBoundingBoxMatch] = field(default_factory=list)


@dataclass_json
@dataclass
class Category:
    id: str
    name: str
    color: str
