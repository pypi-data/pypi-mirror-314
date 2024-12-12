from dataclasses import InitVar, asdict, dataclass, field
from typing import List, Optional

from tenyks_sdk.coco_converters.encryption_utils import sha224_encrypt


@dataclass
class AnnotationInfo:
    coordinates: list[float]
    category_id: int
    segmentation: Optional[list[list[float]]] = None


@dataclass
class Annotation:
    image_key: str
    dataset_key: str
    coordinates: list[float] = field(init=False)
    segmentation: list[list[float]] = field(init=False)
    category_id: int = field(init=False)
    annotation_info: InitVar[AnnotationInfo]
    id: Optional[str] = None
    tags: Optional[List[str]] = field(
        default_factory=list
    )  # [key_value1, key_value2, etc.]

    def __post_init__(self, annotation_info: AnnotationInfo):
        self._extract_annotation_info(annotation_info)
        self.generate_id()

    def _extract_annotation_info(self, annotation_info: AnnotationInfo):
        self.coordinates = list(annotation_info.coordinates)
        self.segmentation = list(annotation_info.segmentation or [])
        self.category_id = annotation_info.category_id

    def generate_id(self):
        if self.id is None:
            list_of_coordinates = self.coordinates + self.segmentation
            hash_string = f"{self.dataset_key}{self.image_key}{str(list_of_coordinates)}{self.category_id}"
            self.id = sha224_encrypt(hash_string)

    def asdict_matching(self):
        result = asdict(self)
        del result["image_key"]
        del result["dataset_key"]
        return result


@dataclass
class Prediction(Annotation):
    model_key: Optional[str] = None
    score: float = 0.0

    def __post_init__(self, annotation_info: AnnotationInfo):
        self._extract_annotation_info(annotation_info)
        self.generate_id()

    def generate_id(self):
        if self.id is None:
            list_of_coordinates = self.coordinates + self.segmentation

            hash_string = f"{self.dataset_key}{self.model_key}{self.image_key}{str(list_of_coordinates)}{self.category_id}"
            self.id = sha224_encrypt(hash_string)

    def asdict_matching(self):
        result = super().asdict_matching()
        del result["model_key"]
        return result
