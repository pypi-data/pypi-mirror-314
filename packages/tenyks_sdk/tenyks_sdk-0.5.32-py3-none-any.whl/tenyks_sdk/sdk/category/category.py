import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Category(BaseModel):
    """
    Represents a category or class that is assigned to objects in the dataset.

    Attributes:
        name (str):
            Name of the category.
            **Examples**: ["cat", "dog", "car"]

        color (Optional[str]):
            Hex color code of the category, typically used for the bounding box color.
            **Examples**: ["#FF0000", "#00FF00", "#0000FF"]
            **Default**: "#000000"

        id (Optional[int]):
            Unique dataset category ID, representing the index of the category in the dataset's categories list.
            **Examples**: [0, 1, 2]
            **Default**: None
            **Constraints**: Must be greater than or equal to 0.
    """

    name: str = Field(
        description="Name of the category",
        examples=["cat", "dog", "car"],
    )
    color: Optional[str] = Field(
        description="Hex color code of the category (the bounding box color).",
        examples=["#FF0000", "#00FF00", "#0000FF"],
        default="#000000",
    )
    id: Optional[int] = Field(
        description="Unique dataset category ID, the index of the category in the dataset categories list",
        examples=[0, 1, 2],
        ge=0,
        default=None,
    )

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v):
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", v):
            raise ValueError("Invalid hex color")
        return v
