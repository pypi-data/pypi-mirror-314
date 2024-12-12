from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Generator

from dataclasses_json import dataclass_json
from tenyks_sdk.utils.tenyks_internal_export import Category
from tenyks_sdk.utils.tenyks_internal_export import TenyksBoundingBox


class TaskType(Enum):
    BBOX = "bbox"
    SEGM = "segm"


class OperateOver(Enum):
    ANNOTATIONS = "annotations"
    PREDICTIONS = "predictions"


class MetricType(Enum):
    MATCHING = "matching"
    BOUNDING_BOX = "bbox"


class MetricAggregation(Enum):
    MEAN = "mean"
    SUM = "sum"
    NONE = "none"
    RECALCULATE = "recalculate"


@dataclass_json
@dataclass
class ModelExportBoundingBoxesLocation:
    model_key: str
    output_location: Dict[str, object]


@dataclass_json
@dataclass
class ModelMetricInput:
    task_id: str
    metric_name: str
    dataset_categories_file_location: Dict[str, object]
    model_folder_locations: List[ModelExportBoundingBoxesLocation]
    metric_results_file_location: Dict[str, object]
    iou_thresholds: Optional[List[float]] = None
    task_type: Optional[TaskType] = field(default=None)


@dataclass_json
@dataclass
class ModelMetricOutput:
    started_at: str
    results: List[Dict]


@dataclass_json
@dataclass
class TenyksBoundingBoxMatchV2:
    image_key: str
    iou: float
    failure_type: str
    annotation: TenyksBoundingBox = field(default=None)
    prediction: TenyksBoundingBox = field(default=None)


@dataclass_json
@dataclass
class TenyksImageInfo:
    image_key: str
    width: int
    height: int


@dataclass_json
@dataclass
class MetricUnifiedInput:
    filter_key: str
    filter_value: str
    images: Generator[TenyksImageInfo, None, None]
    matchings: Generator[TenyksBoundingBoxMatchV2, None, None]
    categories: List[Category]
    task_type: Optional[TaskType] = field(default=None)
    operate_over: Optional[OperateOver] = field(default=None)


@dataclass_json
@dataclass
class MetricUnifiedOutput:
    value: float
