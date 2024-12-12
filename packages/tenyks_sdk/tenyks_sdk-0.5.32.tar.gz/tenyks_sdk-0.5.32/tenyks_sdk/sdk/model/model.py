import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from rich.progress import Progress, SpinnerColumn, TextColumn

from tenyks_sdk.sdk.category import Category
from tenyks_sdk.sdk.client import Client
from tenyks_sdk.sdk.image import Image
from tenyks_sdk.sdk.tag import Tag


class Model(BaseModel):
    """
    Represents a model in the Tenyks platform

    Attributes:
        client (Client): The client to interact with the Tenyks API.
        workspace_name (str): Name of the workspace the model belongs to. Example: `"my_workspace"`.
        dataset_key (str): Key of the dataset the model belongs to. Example: `"my_dataset"`.
        key (str): Key of the model. Example: `"my_model"`.
        name (str): Name of the model. Example: `"My Model"`.
        created_at (datetime): Creation timestamp of the model. Example: `"2024-01-01T00:00:00"`.
        status (str): Status of the model. Examples: `"PENDING"`, `"IN_PROGRESS"`, `"FAILED"`, `"WARNING"`, `"DONE"`.
        dataset_categories (List[Category]): Categories/classes of the dataset the model belongs to.
            Example:
            ```
            [
                Category(id=0, name="person", color="#0000FF"),
                Category(id=1, name="car", color="#FF0000")
            ]
            ```
        dataset_tags (List[Tag]): Tags of the dataset the model belongs to.
            Example:
            ```
            [
                Tag(name="colour", values=["peach"], key="colour"),
                Tag(name="daytime", values=["night", "day"], key="daytime")
            ]
            ```
    """

    client: Client = Field(
        ..., description="The client to interact with the Tenyks API."
    )
    workspace_name: str = Field(
        description="Name of the workspace the model belongs to",
        examples=["my_workspace"],
    )
    dataset_key: str = Field(
        description="Key of the dataset  the model belongs to", examples=["my_dataset"]
    )
    key: str = Field(description="Key of the model", examples=["my_model"])
    name: str = Field(description="Name of the model", examples=["My Model"])
    created_at: datetime = Field(
        description="Creation timestamp of the model",
        examples=["2024-01-01T00:00:00"],
    )
    status: str = Field(
        description="Status of the model",
        examples=["PENDING", "IN_PROGRESS", "FAILED", "WARNING", "DONE"],
    )
    dataset_categories: List[Category] = Field(
        description="Categories/classes of the dataset the model belongs to",
        examples=[
            [
                Category(id=0, name="person", color="#0000FF"),
                Category(id=1, name="car", color="#FF0000"),
            ]
        ],
    )
    dataset_tags: List[Tag] = Field(
        description="Tags of the dataset the model belongs to",
        examples=[
            [
                Tag(name="colour", values=["peach"], key="colour"),
                Tag(
                    name="daytime",
                    values=["night", "day"],
                    key="daytime",
                ),
            ]
        ],
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_model_response(
        cls,
        model_response: Dict,
        client: Client,
        workspace_name: str,
        dataset_key: str,
        dataset_categories: List[Category],
        dataset_tags: List[Tag],
    ) -> "Model":
        timestamp = datetime.strptime(model_response["timestamp"], "%Y-%m-%d-%H.%M.%S")
        return cls(
            key=model_response.get("key"),
            name=model_response.get("display_name"),
            created_at=timestamp,
            status=model_response.get("status"),
            client=client,
            workspace_name=workspace_name,
            dataset_key=dataset_key,
            dataset_categories=dataset_categories,
            dataset_tags=dataset_tags,
        )

    def upload_predictions(
        self, coco_path_or_dict: Union[str, dict], verbose: Optional[bool] = True
    ) -> None:
        file = None
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.dataset_key}/model_inferences/{self.key}/predictions"
        try:
            if isinstance(coco_path_or_dict, str):
                coco_file_path = Path(coco_path_or_dict)
                if not coco_file_path.is_file():
                    raise FileNotFoundError(
                        f"The file '{coco_file_path}' does not exist."
                    )
                file = open(coco_file_path, "rb")
                files = {"file": (coco_file_path.name, file)}

            elif isinstance(coco_path_or_dict, dict):
                json_data = json.dumps(coco_path_or_dict)
                files = {
                    "file": ("coco_annotations.json", json_data, "application/json")
                }
            else:
                raise TypeError(
                    "coco_path_or_dict must be either a file path (str) or a dictionary (dict)"
                )

            if verbose:
                with Progress(
                    SpinnerColumn("aesthetic"),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(
                        description="Uploading predictions...", total=None
                    )
                    self.client.put(endpoint, files=files)
                    self.client.logger.info(
                        f"Successfully uploaded predictions to model '{self.key}'."
                    )
            else:
                self.client.put(endpoint, files=files)
        finally:
            if file:
                file.close()

    def ingest(self) -> None:
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.dataset_key}/model_inferences/{self.key}/ingest"
        self.client.put(endpoint)
        self.client.logger.info(
            f"Successfully triggered ingestion for model '{self.key}'."
        )

    def images_generator(
        self,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
        page_size: Optional[int] = 250,
    ) -> Generator:
        page_number = 0

        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.dataset_key}/model_inferences/{self.key}/images"

        while True:
            params = {
                "filter_by": filter,
                "sort_by": sort_by,
                "page": page_number,
                "size": page_size,
            }
            images_response = self.client.get(endpoint, params=params)
            images = images_response.get("data", [])

            if not images:
                break  # No more images to fetch, exit the loop

            for image in images:
                yield Image.from_image_response(
                    image,
                    self.dataset_tags,
                    self.dataset_categories,
                    convert_to_xywh=True,
                )

            page_number += 1

    def search_images(
        self,
        n_images: Optional[int] = 250,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
    ) -> List[Image]:
        images = []
        page_size = n_images if n_images != -1 else 250
        image_generator = self.images_generator(
            filter=filter, sort_by=sort_by, page_size=page_size
        )
        for image in image_generator:
            images.append(image)
            if n_images != -1 and len(images) >= n_images:
                break
        return images
