from typing import Dict, List, Optional

from pydantic import AliasChoices, BaseModel, Field, HttpUrl, PositiveInt

from tenyks_sdk.sdk.bounding_box import Annotation, Prediction
from tenyks_sdk.sdk.category import Category
from tenyks_sdk.sdk.tag import Tag


class Image(BaseModel):
    """
    Represents an image within a Tenyks dataset.

    Attributes:
        dataset_key (str): Key of the dataset the image belongs to.
            Examples: `my_dataset`.
            Validation Aliases: `dataset_key`, `dataset_name`.

        key (str): Key of the image.
            Examples: `img1`.
            Validation Aliases: `key`, `image_key`.

        filename (str): Filename of the image.
            Examples: `img1.jpg`, `subfolder/img1.png`.

        type (str): Format of the image.
            Examples: `.jpg`, `.png`.
            Validation Aliases: `type`, `image_type`.

        width (PositiveInt): Width of the image in pixels.
            Examples: `1920`, `1080`.

        height (PositiveInt): Height of the image in pixels.
            Examples: `1080`, `720`.

        raw_image_url (HttpUrl): URL to the raw image (e.g., Presigned AWS S3 URL).
            Examples: `https://example.com/image.jpg`.

        tags (Optional[List[Tag]]): List of tags for the image.
            Defaults to an empty list.
            Examples:
                [
                    {
                        "key": "colour",
                        "name": "colour",
                        "values": ["peach"]
                    },
                    {
                        "key": "daytime",
                        "name": "daytime",
                        "values": ["night", "snow"]
                    }
                ].

        annotations (Optional[List[Annotation]]): List of annotations for the image.
            Defaults to an empty list.
            Examples:
                [
                    {
                        "coordinates": [606, 170.91, 621.35, 184.28],
                        "category": {
                            "id": 2,
                            "name": "person",
                            "color": "#FF0000"
                        },
                        "id": "uuid4",
                        "segmentation": [
                            [431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]
                        ],
                        "tags": [
                            {
                                "key": "colour",
                                "name": "colour",
                                "values": ["peach"]
                            }
                        ]
                    }
                ].

        predictions (Optional[List[Prediction]]): List of predictions for the image.
            Defaults to an empty list.
            Examples:
                [
                    {
                        "coordinates": [606, 170.91, 621.35, 184.28],
                        "category": {
                            "id": 2,
                            "name": "person",
                            "color": "#FF0000"
                        },
                        "id": "uuid4",
                        "segmentation": [
                            [431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]
                        ],
                        "tags": [
                            {
                                "key": "colour",
                                "name": "colour",
                                "values": ["peach"]
                            }
                        ],
                        "score": 0.95
                    }
                ].
    """

    dataset_key: str = Field(
        description="Key of the dataset the image belongs to",
        examples=["my_dataset"],
        validation_alias=AliasChoices(
            "dataset_key",
            "dataset_name",
        ),
    )
    key: str = Field(
        description="Key of the image",
        examples=["img1"],
        validation_alias=AliasChoices(
            "key",
            "image_key",
        ),
    )
    filename: str = Field(
        description="Filename of the image",
        examples=["img1.jpg", "subfolder/img1.png"],
    )
    type: str = Field(
        description="Format of the image",
        examples=[".jpg", ".png"],
        validation_alias=AliasChoices(
            "type",
            "image_type",
        ),
    )
    width: PositiveInt = Field(
        description="Width of the image in pixels",
        examples=[1920, 1080],
    )
    height: PositiveInt = Field(
        description="Height of the image in pixels",
        examples=[1080, 720],
    )
    raw_image_url: HttpUrl = Field(
        description="URL to the raw image (e.g. Presigned AWS S3 URL)",
        examples=["https://example.com/image.jpg"],
    )
    tags: Optional[List[Tag]] = Field(
        default_factory=list,
        description="List of tags for the image",
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
    annotations: Optional[List[Annotation]] = Field(
        default_factory=list,
        description="List of annotations for the image",
        examples=[
            [
                Annotation(
                    coordinates=[606, 170.91, 621.35, 184.28],
                    category=Category(id=2, name="person", color="#FF0000"),
                    id="ba2f32418856335fd4a073e0d3217d20d067d7bab983f1b76038c76f",
                    segmentation=[
                        [431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]
                    ],
                    tags=[
                        Tag(key="colour", name="colour", values=["peach"]),
                    ],
                )
            ]
        ],
    )
    predictions: Optional[List[Prediction]] = Field(
        default_factory=list,
        description="List of predictions for the image",
        examples=[
            [
                Prediction(
                    coordinates=[606, 170.91, 621.35, 184.28],
                    category=Category(id=2, name="person", color="#FF0000"),
                    id="ba2f32418856335fd4a073e0d3217d20d067d7bab983f1b76038c76f",
                    segmentation=[
                        [431.0, 217.5, 442.0, 215.5, 432.0, 216.5, 431.0, 217.5]
                    ],
                    tags=[
                        Tag(key="colour", name="colour", values=["peach"]),
                    ],
                    score=0.95,
                )
            ]
        ],
    )

    @classmethod
    def from_image_response(
        cls,
        image_dict: Dict,
        dataset_tags: List[Tag],
        dataset_categories: List[Category],
        convert_to_xywh: bool = False,
    ) -> "Image":
        image_dict["tags"] = [Tag(**tag) for tag in image_dict.get("tags", [])]
        image_dict["annotations"] = [
            Annotation.convert_category_and_create(
                annotation,
                dataset_categories,
                convert_to_xywh=convert_to_xywh,
            )
            for annotation in image_dict.get("annotations", [])
            if annotation.get("bbox_id") or annotation.get("id")
        ]
        image_dict["predictions"] = [
            Prediction.convert_category_and_create(
                prediction,
                dataset_categories,
                convert_to_xywh=convert_to_xywh,
            )
            for prediction in image_dict.get("predictions", [])
            if prediction.get("bbox_id") or prediction.get("id")
        ]
        return cls(**image_dict)
