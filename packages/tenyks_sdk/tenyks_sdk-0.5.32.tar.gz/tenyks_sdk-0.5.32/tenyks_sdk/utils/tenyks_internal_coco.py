# Name pending..
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from werkzeug.utils import secure_filename

from tenyks_sdk.coco_converters.coco_dataset import Category, CocoDataset, Image
from tenyks_sdk.coco_converters.tenyks_dataset import Annotation as TenyksAnnotation
from tenyks_sdk.coco_converters.tenyks_dataset import AnnotationInfo
from tenyks_sdk.coco_converters.tenyks_dataset import Prediction as TenyksPrediction


# move
@dataclass
class TenyksImage(Image):
    image_key: str = field(default=None)


@dataclass
class TenyksInternalCoco:
    dataset_key: str
    model_key: Optional[str]
    image_id_to_key: Dict[str, str]
    images: List[TenyksImage]
    annotations: List[TenyksAnnotation]
    predictions: Optional[List[TenyksPrediction]] = None
    categories: Optional[List[Category]] = None

    @classmethod
    def create_from_coco(
        cls, coco: CocoDataset, dataset_key: str, model_key: str = None
    ):
        cls.dataset_key = dataset_key
        cls.model_key = model_key
        cls.image_id_to_key = TenyksInternalCoco.__map_image_id_to_key(coco.images)
        cls.category_id_to_index = {
            category.id: category_index
            for category_index, category in enumerate(coco.categories)
        }
        cls.images = [
            TenyksImage(**i.to_dict(), image_key=cls.image_id_to_key[i.id])
            for i in coco.images
        ]
        cls.annotations = [
            TenyksAnnotation(
                image_key=cls.image_id_to_key[a.image_id],
                dataset_key=cls.dataset_key,
                annotation_info=AnnotationInfo(
                    coordinates=a.bbox,
                    category_id=cls.category_id_to_index[a.category_id],
                    segmentation=a.segmentation,
                ),
            )
            for a in coco.annotations
        ]

        if model_key and coco.predictions:
            cls.predictions = [
                TenyksPrediction(
                    image_key=cls.image_id_to_key[p.image_id],
                    dataset_key=cls.dataset_key,
                    model_key=cls.model_key,
                    annotation_info=AnnotationInfo(
                        coordinates=p.bbox,
                        category_id=cls.category_id_to_index[p.category_id],
                        segmentation=p.segmentation,
                    ),
                )
                for p in coco.predictions
            ]
        return cls

    @classmethod
    def __map_image_id_to_key(cls, images: List[Image]) -> Dict[str, str]:
        filename_to_id = dict()
        for image in images:
            filename_to_id[image.id] = TenyksInternalCoco.generate_image_id(
                image.file_name
            )
        return filename_to_id

    @staticmethod
    def generate_image_id(image_file_path: str) -> str:
        filename = os.path.basename(image_file_path)
        dir_name = os.path.dirname(image_file_path)
        filename = secure_filename(filename)
        file_name_without_ext, _ = os.path.splitext(filename)

        image_name = os.path.join(dir_name, file_name_without_ext)
        slashes_removed = image_name.replace("/", "_")
        return slashes_removed
