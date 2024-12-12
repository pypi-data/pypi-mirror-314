import logging
from io import BytesIO
from pathlib import Path
from typing import List

from tenyks_sdk.coco_converters.coco_dataset import CocoDataset
from darwin.datatypes import AnnotationClass, AnnotationFile, make_tag
from darwin.importer import get_importer

logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger()
logging.StreamHandler().setFormatter(logging.Formatter("%(asctime)s - %(message)s"))


class CocoToDarwinConverter:
    @staticmethod
    def convert(coco_filepath: str) -> List[AnnotationFile]:
        coco_filepath = Path(coco_filepath)
        coco_dataset = CocoToDarwinConverter.load_coco_dataset_from_file(coco_filepath)

        parser = get_importer("coco")
        parsed_annotation_files = parser(coco_filepath)
        if isinstance(parsed_annotation_files, list):
            if isinstance(parsed_annotation_files[0], list):
                parsed_annotation_files = [
                    item for sublist in parsed_annotation_files for item in sublist
                ]
        else:
            parsed_annotation_files = [parsed_annotation_files]

        parsed_annotation_files = [f for f in parsed_annotation_files if f is not None]

        if coco_dataset.tags:
            filename_to_annotation_file = {
                af.filename: af for af in parsed_annotation_files
            }
            tagged_images = (img for img in coco_dataset.images if img.tags)
            for img in tagged_images:
                annotation_file = filename_to_annotation_file.get(img.file_name)
                if not annotation_file:
                    logger.info(f"No annotation file found for {img.file_name}")
                    continue
                for tag in img.tags:
                    if tag.name == "Default":
                        for tag_value in tag.values:
                            annotation_class_tag = AnnotationClass(tag_value, "tag")
                            annotation_tag = make_tag(tag_value)

                            annotation_file.annotation_classes.add(annotation_class_tag)
                            annotation_file.annotations.append(annotation_tag)

        return parsed_annotation_files

    @staticmethod
    def load_coco_dataset_from_file(file_path: Path) -> CocoDataset:
        with file_path.open("rb") as file:
            byte_stream = BytesIO(file.read())

            coco_dataset = CocoDataset.load(byte_stream)
        return coco_dataset
