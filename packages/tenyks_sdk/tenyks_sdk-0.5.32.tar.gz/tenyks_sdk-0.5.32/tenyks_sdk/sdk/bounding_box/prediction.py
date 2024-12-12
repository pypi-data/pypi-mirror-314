from typing import Dict, List

from pydantic import Field, NonNegativeFloat

from tenyks_sdk.sdk.bounding_box import Annotation
from tenyks_sdk.sdk.category import Category


class Prediction(Annotation):
    """
    Represents a model prediction, including bounding box coordinates, category, segmentation, tags, and a confidence score.

    Attributes:
        coordinates (List[NonNegativeFloat]):
            Bounding box coordinates in the format [x1, y1, x2, y2]. Inherited from `Annotation`.
            **Examples**: [[606, 170.91, 621.35, 184.28]]
            **Constraints**: Must be a list of exactly 4 non-negative floats.

        category (Category):
            The category of the predicted object. Inherited from `Annotation`.
            This should be an instance of the `Category` class.

        id (Optional[str]):
            String ID of the bounding box. It should be unique within the dataset. Inherited from `Annotation`.
            **Examples**: ["uuid4"]
            **Default**: ""
            **Validation Aliases**: "id", "bbox_id"

        segmentation (Optional[List[List[NonNegativeFloat]]]):
            List of (list of) segmentation points for the predicted object. Inherited from `Annotation`.
            **Examples**: [[[431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]]]
            **Default**: An empty list.

        tags (Optional[List[Tag]]):
            List of tags for the bounding box. Each tag can provide additional metadata for the prediction. Inherited from `Annotation`.
            **Examples**:
                - [
                    Tag(key="colour", name="colour", values=["peach"]),
                    Tag(key="daytime", name="daytime", values=["night", "snow"])
                  ]
            **Default**: An empty list.

        score (NonNegativeFloat):
            Confidence score of the prediction.
            **Examples**: [0.75, 1.0, 0.5]
            **Constraints**: Must be a non-negative float and less than or equal to 1.0.
    """

    score: NonNegativeFloat = Field(
        description="Confidence score of the prediction",
        examples=[0.75, 1.0, 0.5],
        le=1.0,
    )

    class Config:
        protected_namespaces = ()  # Override to avoid pydantic warning about model_

    @classmethod
    def convert_category_and_create(
        cls,
        prediction: Dict,
        dataset_categories: List[Category],
        convert_to_xywh: bool = False,
    ):
        prediction_tags = prediction.get("tags", [])
        converted_category = dataset_categories[prediction.get("category_id")]
        if convert_to_xywh:
            prediction["coordinates"] = [
                prediction["coordinates"][0],
                prediction["coordinates"][1],
                prediction["coordinates"][2] - prediction["coordinates"][0],
                prediction["coordinates"][3] - prediction["coordinates"][1],
            ]
        return cls(
            coordinates=prediction.get("coordinates"),
            category=converted_category,
            id=prediction.get("bbox_id") or prediction.get("id"),
            segmentation=prediction.get("segmentation", []),
            tags=prediction_tags,
            score=prediction.get("score"),
        )

    def to_coco_dict(self, image_id: str) -> dict:
        return {
            "id": self.id,
            "image_id": image_id,
            "category_id": self.category.id,
            "bbox": self.coordinates,
            "segmentation": self.segmentation,
            "score": self.score,
            "iscrowd": 0,
            "tags": [tag.model_dump() for tag in self.tags],
        }
