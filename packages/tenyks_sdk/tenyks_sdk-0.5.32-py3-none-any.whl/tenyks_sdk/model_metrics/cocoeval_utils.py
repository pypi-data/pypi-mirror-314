from typing import Dict, List, Tuple, Generator

from tenyks_sdk.model_metrics.datatypes import TaskType, TenyksBoundingBoxMatchV2, TenyksImageInfo
from tenyks_sdk.utils.tenyks_internal_export import (
    Category,
    TenyksBoundingBox,
    TenyksImage,
)


class CocoEvalUtils:

    @staticmethod
    def get_coco_annotations_and_predictions_from_unified_input(
        images: Generator[TenyksImageInfo, None, None],
        matchings: Generator[TenyksBoundingBoxMatchV2, None, None],
        categories: List[Category],
        task_type: TaskType,
    ) -> Tuple[Dict, Dict]:
        assert task_type in [TaskType.BBOX, TaskType.SEGM], "Invalid task type"
        coco_images = []
        coco_annotations = []
        coco_predictions = []
        coco_categories = [{"id": int(cat.id), "name": cat.name} for cat in categories]

        image_info_by_image_id = {image_info.image_key: {
            "width": image_info.width, "height": image_info.height}
            for image_info in images}

        ann_id = 1
        pred_id = 1
        highest_img_idx = 0
        image_key_to_idx_dict = {}

        for matching in matchings:
            image_key = matching.image_key

            if image_key not in image_key_to_idx_dict:
                coco_images.append(
                    {
                        "id": highest_img_idx,
                        "width": image_info_by_image_id[image_key]['width'],
                        "height": image_info_by_image_id[image_key]['height']
                    }
                )
                image_key_to_idx_dict[image_key] = highest_img_idx
                highest_img_idx += 1

            img_idx = image_key_to_idx_dict[image_key]

            ann = matching.annotation
            pred = matching.prediction

            if CocoEvalUtils.__is_valid_annotation_or_prediction(ann, task_type):
                ann_details = CocoEvalUtils.__process_annotation_or_prediction(
                    ann, img_idx, ann_id, is_annotation=True
                )
                coco_annotations.append(ann_details)
                ann_id += 1

            if CocoEvalUtils.__is_valid_annotation_or_prediction(pred, task_type):
                pred_details = CocoEvalUtils.__process_annotation_or_prediction(
                    pred, img_idx, pred_id, is_annotation=False
                )
                coco_predictions.append(pred_details)
                pred_id += 1

        return CocoEvalUtils.__format_coco_data(
            coco_images, coco_annotations, coco_predictions, coco_categories
        )

    @staticmethod
    def get_coco_annotations_and_predictions(
        tenyks_images: List[TenyksImage],
        categories: List[Category],
        task_type: TaskType,
    ) -> Tuple[Dict, Dict]:
        assert task_type in [TaskType.BBOX, TaskType.SEGM], "Invalid task type"
        coco_images = []
        coco_annotations = []
        coco_predictions = []
        coco_categories = [{"id": int(cat.id), "name": cat.name} for cat in categories]

        ann_id = 1
        pred_id = 1

        for img_idx, img in enumerate(tenyks_images):
            image_dict = {"id": img_idx, "width": img.width, "height": img.height}
            coco_images.append(image_dict)

            for match in img.bounding_box_matches:
                ann = match.annotation
                pred = match.prediction

                if CocoEvalUtils.__is_valid_annotation_or_prediction(ann, task_type):
                    ann_details = CocoEvalUtils.__process_annotation_or_prediction(
                        ann, img_idx, ann_id, is_annotation=True
                    )
                    coco_annotations.append(ann_details)
                    ann_id += 1

                if CocoEvalUtils.__is_valid_annotation_or_prediction(pred, task_type):
                    pred_details = CocoEvalUtils.__process_annotation_or_prediction(
                        pred, img_idx, pred_id, is_annotation=False
                    )
                    coco_predictions.append(pred_details)
                    pred_id += 1

        return CocoEvalUtils.__format_coco_data(
            coco_images, coco_annotations, coco_predictions, coco_categories
        )

    @staticmethod
    def __is_valid_annotation_or_prediction(
        annotation: TenyksBoundingBox, task_type: TaskType
    ) -> bool:
        if task_type == TaskType.SEGM and annotation:
            segmentation = annotation.segmentation
            for polygon in segmentation:
                try:
                    polygon_coordinates = list(map(int, polygon))
                    if len(polygon_coordinates) <= 4:
                        return False
                except ValueError:
                    return False

        return (
            annotation
            and annotation.id
            and (
                task_type == TaskType.BBOX
                or (task_type == TaskType.SEGM and annotation.segmentation)
            )
        )

    @staticmethod
    def __process_annotation_or_prediction(
        annotation: TenyksBoundingBox,
        img_idx: int,
        ann_id: int,
        is_annotation: bool,
    ) -> Dict:
        annotation = CocoEvalUtils.__round_coordinates_and_segmentation(annotation)
        coordinates = CocoEvalUtils.__convert_bbox_from_xyxy_to_xywh(
            annotation.coordinates
        )
        area = coordinates[2] * coordinates[3]
        cocoeval_object = {
            "id": ann_id,
            "image_id": img_idx,
            "category_id": int(annotation.category_id),
            "bbox": coordinates,
            "area": area,
            "segmentation": (
                annotation.segmentation if hasattr(annotation, "segmentation") else []
            ),
            "iscrowd": 0,
        }

        if not is_annotation:
            cocoeval_object["score"] = annotation.score

        return cocoeval_object

    @staticmethod
    def __round_coordinates_and_segmentation(annotation: TenyksBoundingBox):
        annotation.coordinates = list(map(int, annotation.coordinates))
        if hasattr(annotation, "segmentation"):
            annotation.segmentation = list(annotation.segmentation)
            for i, polygon in enumerate(annotation.segmentation):
                annotation.segmentation[i] = list(map(int, polygon))

        return annotation

    @staticmethod
    def __convert_bbox_from_xyxy_to_xywh(coordinates: list) -> list:
        x_min, y_min, x_max, y_max = coordinates
        width = x_max - x_min
        height = y_max - y_min
        bbox_xywh = [x_min, y_min, width, height]

        return bbox_xywh

    @staticmethod
    def __format_coco_data(
        images: List[Dict],
        annotations: List[Dict],
        predictions: List[Dict],
        categories: List[Dict],
    ) -> Tuple[Dict, Dict]:
        coco_dataset_annotations = {
            "images": images,
            "annotations": annotations,
            "categories": categories,
        }
        coco_dataset_predictions = {
            "images": images,
            "annotations": predictions,
            "categories": categories,
        }
        return coco_dataset_annotations, coco_dataset_predictions
