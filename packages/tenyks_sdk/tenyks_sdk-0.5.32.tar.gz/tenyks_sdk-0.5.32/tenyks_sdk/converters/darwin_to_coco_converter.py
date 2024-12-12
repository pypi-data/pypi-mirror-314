from typing import Dict, List, Tuple

import cv2
import numpy as np
from pycocotools import mask as maskUtils

from tenyks_sdk.datatypes.coco_dataset import CocoDataset


class DarwinToCocoConverter:

    @staticmethod
    def convert(darwin_images: List[Dict]) -> CocoDataset:
        coco_format: CocoDataset = {
            "images": [],
            "categories": [],
            "annotations": [],
            "tags": [],
        }
        global_tags = set()
        image_id = 0
        annotation_id = 0

        categories, category_mapping, mask_category_mapping = (
            DarwinToCocoConverter.setup_categories(darwin_images)
        )
        coco_format["categories"] = categories

        for item in darwin_images:
            image_details = item["item"]
            annotations = item["annotations"]

            path = image_details["path"]
            path = path.lstrip("/")
            name = image_details["name"]
            filename = f"{path}/{name}" if path else name

            image_default_tag_values = []

            coco_image = {
                "id": image_id,
                "file_name": filename,
                "width": image_details["slots"][0]["width"],
                "height": image_details["slots"][0]["height"],
                "tags": [],
            }

            for ann in annotations:

                if "bounding_box" in ann:
                    bbox_annotation = (
                        DarwinToCocoConverter.create_bounding_box_annotation(
                            ann, annotation_id, image_id, category_mapping[ann["name"]]
                        )
                    )
                    coco_format["annotations"].append(bbox_annotation)
                    annotation_id += 1
                elif "raster_layer" in ann:
                    rle_annotations = (
                        DarwinToCocoConverter.create_raster_layer_annotations(
                            ann["raster_layer"],
                            annotation_id,
                            image_id,
                            coco_image["width"],
                            coco_image["height"],
                            category_mapping,
                            mask_category_mapping,
                        )
                    )
                    coco_format["annotations"].extend(rle_annotations)
                    annotation_id += len(rle_annotations)
                elif "tag" in ann:
                    tag_name = ann["name"]
                    global_tags.add(tag_name)
                    image_default_tag_values.append(tag_name)

            if image_default_tag_values:
                coco_image["tags"] = [
                    {"id": 0, "name": "Default", "values": image_default_tag_values}
                ]

            coco_format["images"].append(coco_image)
            image_id += 1

        if global_tags:
            coco_format["tags"].append(
                {"id": 0, "name": "Default", "values": list(global_tags)}
            )

        return coco_format

    @staticmethod
    def setup_categories(darwin_images: List[Dict]) -> Tuple[List, Dict, Dict]:
        category_id = 0
        category_mapping = {}
        mask_category_mapping = {}
        categories_list = []
        for img in darwin_images:
            annotations = img["annotations"]
            for ann in annotations:
                category_name = None
                if "bounding_box" in ann or "mask" in ann:
                    category_name = ann["name"]
                if "mask" in ann:
                    mask_category_mapping[ann["id"]] = category_name

                if category_name is not None and category_name not in category_mapping:
                    category_mapping[category_name] = category_id
                    categories_list.append({"id": category_id, "name": category_name})
                    category_id += 1

        return categories_list, category_mapping, mask_category_mapping

    @staticmethod
    def create_bounding_box_annotation(
        ann: Dict, annotation_id: int, image_id: int, category_id: int
    ) -> Dict:
        bbox = ann["bounding_box"]
        coco_annotation = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": [bbox["x"], bbox["y"], bbox["w"], bbox["h"]],
            "area": bbox["w"] * bbox["h"],
            "iscrowd": 0,
            "segmentation": [],
        }

        if "polygon" in ann:
            segmentation = DarwinToCocoConverter.get_segmentation_from_polygon(
                ann["polygon"]
            )
            coco_annotation["segmentation"] = segmentation

        return coco_annotation

    @staticmethod
    def get_segmentation_from_polygon(polygon: Dict) -> List:
        segmentation = []
        for path in polygon["paths"]:
            flat_path = [coord for point in path for coord in (point["x"], point["y"])]
            segmentation.append(flat_path)
        return segmentation

    @staticmethod
    def create_raster_layer_annotations(
        raster_layer: Dict,
        annotation_id: int,
        image_id: int,
        image_width: int,
        image_height: int,
        category_mapping: Dict,
        mask_category_mapping: Dict,
    ):
        rle_annotations = []
        dense_rle = raster_layer["dense_rle"]
        mask_annotation_ids_mapping = raster_layer["mask_annotation_ids_mapping"]
        masks = DarwinToCocoConverter.decode_and_split_rle(
            dense_rle,
            mask_category_mapping,
            mask_annotation_ids_mapping,
            image_width,
            image_height,
        )
        for category_name, binary_mask in masks.items():
            encoded_rle = maskUtils.encode(np.asfortranarray(binary_mask))
            polygons = DarwinToCocoConverter.get_polygons_from_rle(encoded_rle)
            coco_annotation = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_mapping[category_name],
                "segmentation": polygons,
                "area": int(maskUtils.area(encoded_rle)),
                "bbox": list(maskUtils.toBbox(encoded_rle)),
                "iscrowd": 0,
            }
            rle_annotations.append(coco_annotation)
        return rle_annotations

    @staticmethod
    def decode_and_split_rle(
        dense_rle, mapping, mask_annotation_ids_mapping, width, height
    ):
        full_mask = DarwinToCocoConverter.decode_dense_rle_to_full_mask(
            dense_rle, width, height
        )
        masks = {}
        for annotation_id, category_index in mask_annotation_ids_mapping.items():
            category_name = mapping[annotation_id]
            binary_mask = (full_mask == category_index).astype(np.uint8)
            masks[category_name] = binary_mask
        return masks

    @staticmethod
    def decode_dense_rle_to_full_mask(dense_rle, width, height):
        full_mask = np.zeros(width * height, dtype=int)
        pos = 0
        for i in range(0, len(dense_rle), 2):
            value = dense_rle[i]
            length = dense_rle[i + 1]
            full_mask[pos : pos + length] = value
            pos += length

        if pos != width * height:
            raise ValueError(
                "The total pixels from the RLE do not match the specified image dimensions."
            )

        full_mask = full_mask.reshape((height, width))

        return full_mask

    @staticmethod
    def get_polygons_from_rle(encoded_rle_segmentation: dict) -> List:
        mask = maskUtils.decode(encoded_rle_segmentation)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        polygons = []
        for contour in contours:
            contour = contour.flatten().tolist()
            if len(contour) > 4:
                polygons.append(contour)

        return polygons
