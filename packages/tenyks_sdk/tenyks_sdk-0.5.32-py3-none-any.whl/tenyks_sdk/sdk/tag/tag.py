from typing import Any, List, Optional, Dict

from pydantic import BaseModel, Field, model_validator


class Tag(BaseModel):
    """
    Represents tags that can be assigned to images or objects.

    Attributes:
        name (str):
            Name of the tag.
            **Examples**: ["Default", "data_slice"]

        values (List[str]):
            List of values for the tag. Each tag can have multiple values.
            **Examples**: [["day", "night"]]

        key (Optional[str]):
            String ID of the tag. It should be unique within the dataset.
            This field is excluded from output serialization.
            **Examples**: ["Default", "data_slice"]
    """

    name: str = Field(
        description="Name of the tag.",
        examples=["Default", "data_slice"],
    )
    values: List[str] = Field(
        description="List of values for the tag. Each tag can have multiple values.",
        examples=[["day", "night"]],
    )
    key: Optional[str] = Field(
        description="String ID of the tag. It should be unique within the dataset.",
        examples=["Default", "data_slice"],
        exclude=True,
    )

    @model_validator(mode="before")
    @classmethod
    def validate_key(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "key" not in values:
            values["key"] = values["name"].replace(" ", "_")
        return values
