from typing import Dict, List, Optional

from pydantic import AliasChoices, BaseModel, Field, NonNegativeFloat

from tenyks_sdk.sdk.category import Category
from tenyks_sdk.sdk.tag import Tag


class Annotation(BaseModel):
    """
    Represents an image annotation, including bounding box coordinates, category, segmentation, and tags.

    Attributes:
        coordinates (List[NonNegativeFloat]):
            Bounding box coordinates in the format [x1, y1, x2, y2].
            **Examples**: [[606, 170.91, 621.35, 184.28]]
            **Constraints**: Must be a list of exactly 4 non-negative floats.

        category (Category):
            The category of the annotated object. This should be an instance of the `Category` class.

        id (Optional[str]):
            String ID of the bounding box. It should be unique within the dataset.
            **Examples**: ["uuid4"]
            **Default**: ""
            **Validation Aliases**: "id", "bbox_id"

        segmentation (Optional[List[List[NonNegativeFloat]]]):
            List of (list of) segmentation points for the annotated object.
            **Examples**: [[[431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]]]
            **Default**: An empty list.

        tags (Optional[List[Tag]]):
            List of tags for the bounding box. Each tag can provide additional metadata for the annotation.
            **Examples**:
                - [
                    Tag(key="colour", name="colour", values=["peach"]),
                    Tag(key="daytime", name="daytime", values=["night", "snow"])
                  ]
            **Default**: An empty list.
    """

    coordinates: List[NonNegativeFloat] = Field(
        description="Bounding box coordinates in the format [x1, y1, x2, y2].",
        examples=[[606, 170.91, 621.35, 184.28]],
        min_length=4,
        max_length=4,
    )
    category: Category
    id: Optional[str] = Field(
        default="",
        description="String ID of the bounding box. It should be unique within the dataset.",
        examples=["ba2f32418856335fd4a073e0d3217d20d067d7bab983f1b76038c76f"],
        validation_alias=AliasChoices(
            "id",
            "bbox_id",
        ),
    )
    segmentation: Optional[List[List[NonNegativeFloat]]] = Field(
        default_factory=list,
        description="List of (list of) segmentation points.",
        examples=[[[431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]]],
    )
    tags: Optional[List[Tag]] = Field(
        default_factory=list,
        description="List of tags for the bounding box.",
        examples=[
            [
                Tag(key="colour", name="colour", values=["peach"]),
                Tag(
                    key="daytime",
                    name="daytime",
                    values=[
                        "night",
                        "snow",
                    ],
                ),
            ]
        ],
    )

    @classmethod
    def convert_category_and_create(
        cls,
        annotation: Dict,
        dataset_categories: List[Category],
        convert_to_xywh: bool = False,
    ):
        annotation_tags = annotation.get("tags", [])
        converted_category = dataset_categories[annotation.get("category_id")]
        if convert_to_xywh:
            annotation["coordinates"] = [
                annotation["coordinates"][0],
                annotation["coordinates"][1],
                annotation["coordinates"][2] - annotation["coordinates"][0],
                annotation["coordinates"][3] - annotation["coordinates"][1],
            ]
        return cls(
            coordinates=annotation.get("coordinates"),
            category=converted_category,
            id=annotation.get("bbox_id") or annotation.get("id"),
            segmentation=annotation.get("segmentation", []),
            tags=annotation_tags,
        )

    def to_coco_dict(self, image_id: str) -> dict:
        return {
            "id": self.id,
            "image_id": image_id,
            "category_id": self.category.id,
            "bbox": self.coordinates,
            "segmentation": self.segmentation,
            "iscrowd": 0,
            "tags": [tag.model_dump() for tag in self.tags],
        }
