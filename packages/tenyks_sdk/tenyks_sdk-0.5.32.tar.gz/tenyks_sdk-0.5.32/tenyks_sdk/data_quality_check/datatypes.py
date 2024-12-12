from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Union

from dataclasses_json import dataclass_json


class Severity(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    def __str__(self):
        return str(self.value)


class DQCCheckStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def __str__(self):
        return str(self.value)


class DQCCheckResultType(Enum):
    IMAGE = "image"
    ANNOTATION = "annotation"

    def __str__(self):
        return str(self.value)


@dataclass_json
@dataclass
class DQCIndividualCheckResultImage:
    image_id: List[str]
    severity: Severity
    description: str = field(default="")
    type: DQCCheckResultType = field(default=DQCCheckResultType.IMAGE)


@dataclass_json
@dataclass
class DQCIndividualCheckResultAnnotation:
    annotation_id: List[str]
    severity: Severity
    description: str = field(default="")
    type: DQCCheckResultType = field(default=DQCCheckResultType.ANNOTATION)


DQCIndividualCheckResult = Union[
    DQCIndividualCheckResultImage, DQCIndividualCheckResultAnnotation
]


@dataclass_json
@dataclass
class DQCCheckResult:
    type: Union[Enum, str]
    display_name: str
    version: str
    description: str
    results: List[DQCIndividualCheckResult]
    started_at: str
    completed_at: str
    status: DQCCheckStatus
    errors: List[str] = field(default_factory=list)


@dataclass_json
@dataclass
class DQCOutput:
    job_id: str
    job_started_at: str
    output_assembled_at: str
    checks: List[DQCCheckResult]


@dataclass_json
@dataclass
class DQCInput:
    job_id: str
    coco_location: Dict[str, object]
    output_location: Dict[str, object]
    check_types: List[str] = field(default_factory=list)
    dataset_key: str = field(default="")  # TODO: To be removed soon
    # Additional input parameters needed?


class DqcRunsOn(Enum):
    DATASET = "dataset"
    MODEL = "model"

    def __str__(self):
        return str(self.value)


class DqcDependency(Enum):
    IMAGE_EMBEDDINGS = "image_embedding"
    OBJECT_EMBEDDINGS = "object_embeddings"
    MATCHINGS = "matchings"
    ANNOTATIONS = "annotations"

    def __str__(self):
        return str(self.value)
