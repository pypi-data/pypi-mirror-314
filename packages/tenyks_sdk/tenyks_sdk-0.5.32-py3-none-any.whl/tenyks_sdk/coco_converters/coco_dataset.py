from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Any, List, Optional, Union

import cv2
import orjson
from fastclasses_json import dataclass_json
from pycocotools import mask as maskUtils


@dataclass_json
@dataclass
class Info:
    year: Optional[int] = None
    version: Optional[str] = None
    description: Optional[str] = None
    contributor: Optional[str] = None
    url: Optional[str] = None
    date_created: Optional[str] = None


@dataclass_json
@dataclass
class License:
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None


@dataclass_json
@dataclass
class Tag:
    id: Optional[int] = None
    name: Optional[str] = None
    values: Optional[List[str]] = None


@dataclass_json
@dataclass
class Image:
    id: Optional[int] = None
    file_name: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    date_captured: Optional[str] = None
    license: Optional[int] = None
    flickr_url: Optional[str] = None
    coco_url: Optional[str] = None
    tags: Optional[List[Tag]] = None


@dataclass_json
@dataclass
class Annotation:
    id: Optional[int] = None
    image_id: Optional[int] = None
    category_id: Optional[int] = None
    bbox: Optional[List[float]] = None
    iscrowd: Optional[int] = None
    segmentation: Optional[Any] = None
    area: Optional[float] = None
    tags: Optional[List[Tag]] = None


@dataclass_json
@dataclass
class Prediction(Annotation):
    score: Optional[float] = 1.0


@dataclass_json
@dataclass
class Category:
    id: Optional[int] = None
    name: Optional[str] = None
    supercategory: Optional[str] = None


class BoundingBoxCoordinatesFormat(Enum):
    XYXY = "xyxy"
    XYWH = "xywh"


@dataclass_json
@dataclass
class CocoDataset:
    images: Optional[List[Image]] = None
    categories: Optional[List[Category]] = None
    info: Optional[Info] = None
    licenses: Optional[List[License]] = None
    annotations: Optional[List[Annotation]] = None
    predictions: Optional[List[Prediction]] = None
    tags: Optional[List[Tag]] = None

    def export(self, fast_json_serializer=False, **kwargs):
        if fast_json_serializer:
            return orjson.dumps(self.to_dict(), option=orjson.OPT_SERIALIZE_NUMPY)
        return self.to_json(**kwargs)

    @classmethod
    def load(cls, stream: BytesIO):
        coco_dataset = cls.from_json(stream.read())

        return coco_dataset

    @classmethod
    def load_and_convert(cls, stream: BytesIO):
        coco_dataset = cls.from_json(stream.read())
        bbox_format_converter = BoundingBoxFormatConverter()
        segmentation_converter = SegmentationFormatConverter()

        if coco_dataset.annotations is not None:

            coco_dataset.annotations = (
                bbox_format_converter.convert_bbox_to_xyxy_format(
                    coco_dataset.annotations
                )
            )

            coco_dataset.annotations = segmentation_converter.convert_rle_to_polygon(
                coco_dataset.annotations
            )
            coco_dataset.annotations = (
                segmentation_converter.clamp_segmentation_polygons(
                    coco_dataset.annotations
                )
            )

        if coco_dataset.predictions is not None:

            coco_dataset.predictions = (
                bbox_format_converter.convert_bbox_to_xyxy_format(
                    coco_dataset.predictions
                )
            )

            coco_dataset.predictions = segmentation_converter.convert_rle_to_polygon(
                coco_dataset.predictions
            )
            coco_dataset.predictions = (
                segmentation_converter.clamp_segmentation_polygons(
                    coco_dataset.predictions
                )
            )

        return coco_dataset


class BoundingBoxFormatConverter:
    def convert_bbox_to_xyxy_format(
        self, annotations: List[Annotation]
    ) -> List[Annotation]:
        for annotation in annotations:
            bbox = list(annotation.bbox)
            bbox[2] += bbox[0]
            bbox[3] += bbox[1]
            bbox = [max(0.0, x) for x in bbox]
            annotation.bbox = tuple(bbox)

        return annotations

    def check_xyxy_format(self, annotations: List[Annotation]) -> bool:
        for annotation in annotations:
            # xywh format
            bbox = annotation.bbox
            if (bbox[3] < bbox[1]) or (bbox[2] < bbox[0]):
                return False

        return True


class SegmentationFormatConverter:

    def clamp_segmentation_polygons(
        self, annotations: List[Annotation]
    ) -> List[Annotation]:
        for annotation in annotations:
            if annotation.segmentation is not None:
                clamped_segmentations = []
                for polygon in annotation.segmentation:
                    clamped_polygon = [max(0, coordinate) for coordinate in polygon]
                    clamped_segmentations.append(clamped_polygon)

                annotation.segmentation = clamped_segmentations

        return annotations

    def convert_rle_to_polygon(self, annotations: List[Annotation]) -> List[Annotation]:
        for annotation in annotations:
            if annotation.segmentation is not None:
                is_rle_format = isinstance(annotation.segmentation, dict)
                if is_rle_format:
                    encoded_rle_segmentation = self.__convert_to_encoded_rle_format(
                        annotation.segmentation
                    )
                    polygons = self.__get_polygons_from_rle(encoded_rle_segmentation)
                    annotation.segmentation = polygons

        return annotations

    def __convert_to_encoded_rle_format(self, segmentation: Union[list, dict]):
        assert (
            "size" in segmentation and "counts" in segmentation
        ), "Segmentation dict must contain 'size' and 'counts'."

        is_decompressed = isinstance(segmentation["counts"], list)
        if is_decompressed:
            height, width = segmentation["size"]
            return maskUtils.frPyObjects(segmentation, height, width)
        else:
            return segmentation

    def __get_polygons_from_rle(self, encoded_rle_segmentation: dict) -> List:
        mask = maskUtils.decode(encoded_rle_segmentation)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        polygons = []
        for contour in contours:
            contour = contour.flatten().tolist()
            if len(contour) > 4:
                polygons.append(contour)

        return polygons
