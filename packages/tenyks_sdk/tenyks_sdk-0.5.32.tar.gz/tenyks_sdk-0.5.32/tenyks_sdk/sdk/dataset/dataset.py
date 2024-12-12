import json
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Generator, List, Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from rich.progress import Progress, SpinnerColumn, TextColumn

from tenyks_sdk.converters.json_to_arrow_converter import JsonArrowConverter
from tenyks_sdk.file_providers.location_builder.location_builder_factory import (
    LocationBuilderFactory,
)
from tenyks_sdk.sdk.bounding_box.annotation import Annotation
from tenyks_sdk.sdk.category import Category
from tenyks_sdk.sdk.client import Client
from tenyks_sdk.sdk.cloud import AWSCredentials, AWSLocation, AzureLocation, GCSLocation
from tenyks_sdk.sdk.dataset.image_upload_manager import ImageUploadManager
from tenyks_sdk.sdk.dataset.utils import split_dict_into_batches
from tenyks_sdk.sdk.image import Image
from tenyks_sdk.sdk.video import VideoClip
from tenyks_sdk.sdk.model.model import Model
from tenyks_sdk.sdk.tag import Tag


class ImportOperation(Enum):
    APPEND = "APPEND"
    OVERWRITE_IMAGES = "OVERWRITE_IMAGES"
    OVERWRITE_DATASET = "OVERWRITE_DATASET"


class Dataset(BaseModel):
    """
    A dataset class representing a dataset in the Tenyks platform

    Attributes:
        client (Client): The client to interact with the Tenyks API.
        workspace_name (str): Name of the workspace the dataset belongs to.
        key (str): Key of the dataset.
        name (str): Name of the dataset.
        owner (str): Owner of the dataset.
        owner_email (EmailStr): Owner email of the dataset.
        created_at (datetime): Creation timestamp of the dataset.
        images_location (Optional[Union[AWSLocation, AzureLocation, GCSLocation]]): Directory location of the images of the dataset.
        metadata_location (Optional[Union[AWSLocation, AzureLocation, GCSLocation]]): Directory location of the metadata of the dataset.
        categories (List[Category]): Categories/classes of the dataset.
        models (List): Names of the models of the dataset.
        status (str): Status of the dataset.
        n_images (int): Number of images in the dataset.
        iou_threshold (float): IOU threshold set for the dataset.
    """

    client: Client = Field(
        ..., description="The client to interact with the Tenyks API."
    )
    workspace_name: str = Field(
        description="Name of the workspace the dataset belongs to",
        examples=["my_workspace"],
    )
    key: str = Field(description="Key of the dataset", examples=["my_dataset"])
    name: str = Field(description="Name of the dataset", examples=["My Dataset"])
    owner: str = Field(description="Owner of the dataset", examples=["My Dataset"])
    owner_email: EmailStr = Field(
        description="Owner email of the dataset", examples=["user@mail.com"]
    )
    created_at: datetime = Field(
        description="Creation timestamp of the dataset",
        examples=["2024-01-01T00:00:00"],
    )
    images_location: Optional[Union[AWSLocation, AzureLocation, GCSLocation]] = Field(
        description="Directory location of the images of the dataset",
        examples=[
            AWSLocation(
                type="aws_s3",
                s3_uri="s3://bucket/xxx/xxx/images/",
                credentials=AWSCredentials(
                    aws_access_key_id="YOUR_ACCESS_KEY",
                    aws_secret_access_key="YOUR_SECRET_KEY",
                    region_name="YOUR_REGION",
                ),
            )
        ],
    )
    metadata_location: Optional[Union[AWSLocation, AzureLocation, GCSLocation]] = Field(
        description="Directory location of the metadata of the dataset",
        examples=[
            AWSLocation(
                type="aws_s3",
                s3_uri="s3://bucket/xxx/xxx/metadata/",
                credentials=AWSCredentials(
                    aws_access_key_id="YOUR_ACCESS_KEY",
                    aws_secret_access_key="YOUR_SECRET_KEY",
                    region_name="YOUR_REGION",
                ),
            )
        ],
    )
    categories: List[Category] = Field(
        description="Categories/classes of the dataset",
        examples=[
            [
                Category(id=0, name="person", color="#0000FF"),
                Category(id=1, name="car", color="#FF0000"),
            ]
        ],
    )
    models: List = Field(
        description="Names of the models of the dataset",
        examples=[["model1", "model2"]],
    )
    status: str = Field(
        description="Status of the dataset",
        examples=["PENDING", "IN_PROGRESS", "FAILED", "WARNING", "DONE"],
    )
    n_images: int = Field(description="Number of images in the dataset", examples=[100])
    iou_threshold: float = Field(
        description="IOU threshold set for the dataset", examples=[0.5]
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_dataset_response(
        cls,
        dataset_response: Dict,
        client: Client,
        workspace_name: str,
    ) -> "Dataset":
        def create_location(
            location_data: Dict,
        ) -> Optional[Union[AWSLocation, AzureLocation, GCSLocation]]:
            if "s3_uri" in location_data:
                return AWSLocation(**location_data)
            elif "azure_uri" in location_data:
                return AzureLocation(**location_data)
            elif "gcs_uri" in location_data:
                return GCSLocation(**location_data)
            else:
                return None

        categories = dataset_response.get("categories", [])
        categories = [
            Category(id=idx, name=category["name"], color=category["color"])
            for idx, category in enumerate(categories)
        ]
        model_names = [
            model["key"] for model in dataset_response.get("model_inferences", [])
        ]
        timestamp = datetime.strptime(
            dataset_response.get("timestamp"), "%Y-%m-%d-%H.%M.%S"
        )

        images_location_data = dataset_response.get("images_location", {})
        metadata_location_data = dataset_response.get("metadata_location", {})

        images_location = (
            create_location(images_location_data) if images_location_data else None
        )
        metadata_location = (
            create_location(metadata_location_data) if metadata_location_data else None
        )

        return cls(
            client=client,
            workspace_name=workspace_name,
            key=dataset_response.get("key"),
            name=dataset_response.get("dataset_name"),
            owner=dataset_response.get("owner"),
            owner_email=dataset_response.get("owner_email"),
            created_at=timestamp,
            images_location=images_location,
            metadata_location=metadata_location,
            categories=categories,
            models=model_names,
            status=dataset_response.get("status"),
            n_images=dataset_response.get("size"),
            iou_threshold=dataset_response.get("iou_threshold"),
        )

    @property
    def tags(self) -> List[Tag]:
        return self.get_tags()

    def get_tags(self) -> List[Tag]:
        """Retrieve the tags associated with the dataset.

        Returns:
            List[Tag]: A list of tags created for the dataset.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/tags"
        tags_response = self.client.get(endpoint)
        return [Tag(**tag) for tag in tags_response.get("tags")]

    def get_category_by_id(self, category_id: int) -> Category:
        """Retrieve a category by its ID.

        Args:
            category_id (int): The ID of the category to retrieve.

        Raises:
            ValueError: If no category with the given ID is found.

        Returns:
            Category: The category corresponding to the given ID.
        """
        category = next(
            (category for category in self.categories if category.id == category_id),
            None,
        )
        if category is None:
            raise ValueError(f"Category with id {category_id} not found.")
        return category

    def get_category_by_name(self, category_name: str) -> Category:
        """Retrieve a category by its name.

        Args:
            category_name (str): The name of the category to retrieve.

        Raises:
            ValueError: If no category with the given name is found.

        Returns:
            Category: The category corresponding to the given name.
        """
        category = next(
            (
                category
                for category in self.categories
                if category.name == category_name
            ),
            None,
        )
        if category is None:
            raise ValueError(f"Category '{category_name}' not found.")
        return category

    def get_tag_by_key(self, tag_key: str) -> Tag:
        """Retrieve a tag by its key.

        Args:
            tag_key (str): The key of the tag to retrieve.

        Raises:
            ValueError: If no tag with the given key is found.

        Returns:
            Tag: The tag corresponding to the given key.
        """
        tag = next((tag for tag in self.tags if tag.key == tag_key), None)
        if tag is None:
            raise ValueError(f"Tag with key '{tag_key}' not found.")
        return tag

    def get_tag_by_name(self, tag_name: str) -> Tag:
        """Retrieve a tag by its display name.

        Args:
            tag_name (str): The name of the tag to retrieve.

        Raises:
            ValueError: If no tag with the given name is found.

        Returns:
            Tag: The tag corresponding to the given display name.
        """
        tag = next((tag for tag in self.tags if tag.name == tag_name), None)
        if tag is None:
            raise ValueError(f"Tag '{tag_name}' not found.")
        return tag

    def get_image_by_key(self, image_key: str) -> Image:
        """Retrieve an image by its key.

        Args:
            image_key (str): The key of the image to retrieve.

        Raises:
            ValueError: If no image with the given key is found.

        Returns:
            Image: The image corresponding to the given key.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/images"
        filter = f"image_key:[{image_key}]"
        params = {
            "filter_by": filter,
            "page": 0,
            "size": 1,
        }
        images_response = self.client.get(endpoint, params=params)
        images_response_list = images_response.get("data")

        if len(images_response_list):
            return Image.from_image_response(
                images_response_list[0],
                self.tags,
                self.categories,
                convert_to_xywh=True,
            )
        else:
            raise ValueError(f"Image with key {image_key} not found.")

    def add_number_of_images(self, n_images: int) -> None:
        self.n_images += n_images

    def upload_images(
        self,
        image_directory_or_paths: Union[str, Path, List[str]],
        verbose: Optional[bool] = True,
    ) -> None:
        """Upload images to the dataset.

        Args:
            image_directory_or_paths (Union[str, Path, List[str]]): The directory or paths of the images to upload.
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to True.

        Raises:
            TypeError: If the input type for image_directory_or_paths is not str, Path, or List[str].
        """
        image_upload_manager = ImageUploadManager(self.client)
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/images/files"

        if isinstance(image_directory_or_paths, str):
            image_directory_or_paths = Path(image_directory_or_paths)

        if isinstance(image_directory_or_paths, Path):
            if image_directory_or_paths.is_dir():
                successfully_uploaded_images, failed_to_upload_images = (
                    image_upload_manager.upload_files(
                        image_directory_or_paths, endpoint, verbose=verbose
                    )
                )
            else:
                image_paths = [image_directory_or_paths]
                successfully_uploaded_images, failed_to_upload_images = (
                    image_upload_manager.upload_files(image_paths, endpoint)
                )
        elif isinstance(image_directory_or_paths, list):
            image_paths = [Path(image_path) for image_path in image_directory_or_paths]
            successfully_uploaded_images, failed_to_upload_images = (
                image_upload_manager.upload_files(image_paths, endpoint)
            )
        else:
            raise TypeError(
                "image_directory_or_image_paths must be a str, Path, or list of str"
            )

        self.add_number_of_images(len(successfully_uploaded_images))
        if verbose:
            self.client.logger.info(
                f"Successfully uploaded {len(successfully_uploaded_images)} images "
                f"and failed to upload {len(failed_to_upload_images)} images "
                f"to dataset {self.key}."
            )

    def upload_annotations(
        self, coco_path_or_dict: Union[str, dict], verbose: Optional[bool] = True
    ) -> None:
        """Upload annotations to the dataset.

        Args:
            coco_path_or_dict (Union[str, dict]): The file path or dictionary of COCO annotations to upload.
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to True.

        Raises:
            FileNotFoundError: If the provided file path does not exist.
            TypeError: If the input type for coco_path_or_dict is not str or dict.
        """
        endpoint = (
            f"/workspaces/{self.workspace_name}/datasets/{self.key}/images/annotations"
        )

        file = None
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
                        description="Uploading annotations...", total=None
                    )
                    self.client.put(endpoint, files=files)
                    self.client.logger.info(
                        f"Successfully uploaded annotations to dataset '{self.key}'."
                    )
            else:
                self.client.put(endpoint, files=files)
        finally:
            if file:
                file.close()

    def upload_annotations_from_cloud(
        self, coco_file_location: Union[AWSLocation, AzureLocation, GCSLocation]
    ) -> None:
        """Upload annotations to the dataset from a cloud location.

        Args:
            coco_file_location (Union[AWSLocation, AzureLocation, GCSLocation]): The cloud location of the COCO annotations to upload.
        """
        endpoint = (
            f"/workspaces/{self.workspace_name}/datasets/{self.key}/images/annotations"
        )
        self.client.put(endpoint, body=coco_file_location.model_dump())
        self.client.logger.info(
            f"Successfully uploaded annotations to dataset '{self.key}' from cloud provider."
        )

    def add_image(
        self,
        image_path: str,
        annotations: Optional[List[Annotation]] = None,
        tags: Optional[List[Tag]] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        """Add an image to the dataset along with its annotations and tags.

        Args:
            image_path (str): The path of the image to add.
            annotations (Optional[List[Annotation]], optional): The annotations to add to the image. Defaults to None.
            tags (Optional[List[Tag]], optional): The tags to add to the image. Defaults to None.
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to False.
        """
        image_path = Path(image_path)
        coco_dict = self._create_image_coco_dict(image_path.name, annotations, tags)
        self.upload_images(image_path, verbose=verbose)
        self.upload_annotations(coco_dict, verbose=verbose)
        self.ingest(import_operation="OVERWRITE_IMAGES", verbose=verbose)

    def update_image(
        self,
        image_key: str,
        annotations: List[Annotation],
        tags: Optional[List[Tag]] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        """Update an existing image's annotations and tags.

        Args:
            image_key (str): The key of the image to update.
            annotations (List[Annotation]): The new annotations for the image.
            tags (Optional[List[Tag]], optional): The new tags for the image. Defaults to None.
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to False.
        """
        image = self.get_image_by_key(image_key)
        coco_dict = self._create_image_coco_dict(image.filename, annotations, tags)
        self.upload_annotations(coco_dict, verbose=verbose)
        self.ingest(import_operation="OVERWRITE_IMAGES", verbose=verbose)

    def ingest(
        self, import_operation: Optional[str] = None, verbose: Optional[bool] = True
    ) -> None:
        """Trigger the ingestion process for the dataset.

        Args:
            import_operation (Optional[str], optional): The import operation type. Defaults to None.
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to True.

        Raises:
            ValueError: If the provided import operation is invalid.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/ingest"
        payload = {}
        if import_operation:
            if import_operation not in ImportOperation.__members__:
                raise ValueError(
                    f"Invalid import_operation: {import_operation}. Must be one of {list(ImportOperation.__members__.keys())}."
                )
            payload["import_operation"] = import_operation

        self.client.put(endpoint, body=payload)
        if verbose:
            self.client.logger.info(
                f"Successfully triggered ingestion for dataset '{self.key}'."
            )

    def get_models(self) -> List[Model]:
        """Retrieve the models associated with the dataset.

        Returns:
            List[Model]: A list of models associated with the dataset.
        """
        endpoint = (
            f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences"
        )
        models_response = self.client.get(endpoint)
        return [
            Model.from_model_response(
                {**model},
                client=self.client,
                workspace_name=self.workspace_name,
                dataset_key=self.key,
                dataset_categories=self.categories,
                dataset_tags=self.tags,
            )
            for model in models_response
        ]

    def get_model_names(self) -> List[str]:
        """Retrieve the names of the models associated with the dataset.

        Returns:
            List[str]: A list of model display names.
        """
        models = self.get_models()
        return [model.name for model in models]

    def get_model(self, key: str) -> Model:
        """Retrieve a model by its key.

        Args:
            key (str): The key of the model to retrieve.

        Returns:
            Model: The model corresponding to the given key.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences/{key}"
        model_response = self.client.get(endpoint)
        return Model.from_model_response(
            {**model_response},
            client=self.client,
            workspace_name=self.workspace_name,
            dataset_key=self.key,
            dataset_categories=self.categories,
            dataset_tags=self.tags,
        )

    def create_model(
        self,
        name: str,
        confidence_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None,
    ) -> Model:
        """Create a new model for the  dataset.

        Args:
            name (str): The name of the new model.
            confidence_threshold (Optional[float], optional): The confidence threshold for the model. Defaults to None.
            iou_threshold (Optional[float], optional): The IOU threshold for the model. Defaults to None.

        Returns:
            Model: The newly created model.
        """
        endpoint = (
            f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences"
        )
        payload = {
            "key": name.lower(),
            "display_name": name,
        }
        if confidence_threshold:
            payload["confidence_threshold"] = confidence_threshold
        if iou_threshold:
            payload["iou_threshold"] = iou_threshold
        model_response = self.client.post(endpoint, body=payload)
        model = Model.from_model_response(
            {**model_response},
            client=self.client,
            workspace_name=self.workspace_name,
            dataset_key=self.key,
            dataset_categories=self.categories,
            dataset_tags=self.tags,
        )
        self.client.logger.info(
            f"Model '{name}' created successfully with key {model.key}."
        )
        return model

    def delete_model(self, key: str) -> None:
        """Delete a model from the dataset.

        Args:
            key (str): The key of the model to delete.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences/{key}"
        self.client.delete(endpoint)
        self.client.logger.info(f"Model {key} deleted successfully.")

    def head(self, n: int = 5) -> List[Image]:
        """Retrieve the first few images from the dataset.

        Args:
            n (int, optional): The number of images to retrieve. Defaults to 5.

        Returns:
            List[Image]: A list of the first `n` images in the dataset.
        """
        return self.search_images(n_images=n)

    def search_images(
        self,
        n_images: Optional[int] = 250,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
        model_key: Optional[str] = None,
    ) -> List[Image]:
        """Perform image search in the dataset based on filters.

        Args:
            n_images (Optional[int], optional): The number of images to retrieve. Defaults to 250.
            filter (Optional[str], optional): Filter conditions for the search. Defaults to None.
            sort_by (Optional[str], optional): Sort criteria for the search. Defaults to None.
            model_key (Optional[str], optional): Model key to filter images. Defaults to None.

        Returns:
            List[Image]: A list of images that match the search criteria.
        """
        images = []
        page_size = n_images if n_images != -1 else 250
        image_generator = self.images_generator(
            filter=filter, sort_by=sort_by, model_key=model_key, page_size=page_size
        )
        for image in image_generator:
            images.append(image)
            if n_images != -1 and len(images) >= n_images:
                break
        return images

    def images_generator(
        self,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
        model_key: Optional[str] = None,
        page_size: Optional[int] = 250,
    ) -> Generator:
        """Generator to retrieve images from the dataset in a paginated manner.

        Args:
            filter (Optional[str], optional): Filter conditions for the search. Defaults to None.
            sort_by (Optional[str], optional): Sort criteria for the search. Defaults to None.
            model_key (Optional[str], optional): Model key to filter images. Defaults to None.
            page_size (Optional[int], optional): Number of images per page. Defaults to 250.

        Yields:
            Generator: A generator yielding images.
        """
        page_number = 0
        dataset_tags = self.tags
        dataset_categories = self.categories

        if model_key:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences/{model_key}/images"
        else:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/images"
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
                    image, dataset_tags, dataset_categories, convert_to_xywh=True
                )

            page_number += 1

    def finetune_search_model(
            self,
            search_query: str,
            ground_truth_search_results: List[Image]
    ):
        """
        Placeholder method for finetuning search

        Args:
            search_query (str): search query on which to finetune model
            ground_truth_search_results (List[Image]): ground truth images that should be retrieved
        """
        s = ("This feature is currently available only to private beta-customers. "
        "Please contact support if you are interested in experimenting with early-stage "
        "Tenkys Search experiences and share feedback.")
        print(s)

    def count_images(
        self, filter: Optional[str] = None, model_key: Optional[str] = None
    ) -> int:
        """Return image count that match the filter criteria.

        Args:
            filter (Optional[str], optional): Filter conditions for counting. Defaults to None.
            model_key (Optional[str], optional): Model key to filter images. Defaults to None.

        Returns:
            int: Number of images that match the filter criteria.
        """
        if model_key:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences/{model_key}/images"
        else:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/images"

        params = {
            "filter_by": filter,
            "include_total_count": True,
            "page": 0,
            "size": 1,
        }
        images_response = self.client.get(endpoint, params=params)
        total_count = images_response.get("total_count", 0)
        return total_count

    def save_image_metadata(
        self, metadata_key: str, metadata_values: Dict[str, Union[int, float]]
    ) -> None:
        """
        Add or update custom metadata for images in a dataset.

        Args:
            metadata_key (str): The key representing the type of metadata to be saved.
                Must contain only alphanumeric characters (no spaces, underscores,
                or special characters), e.g. brightness.
            metadata_values (Dict[str, Union[int, float]]): A dictionary where the keys
                are image identifiers and the values are the metadata values to be saved
                (either integer or float).

        Raises:
            ValueError: If the 'metadata_key' contains invalid characters or if any
                value in 'metadata_values' is not an integer or a float.

        Example:
            metadata_values = {
                "image1": 0.75,
                "image2": 0.85,
                "image3": 0.65,
                # More image metadata...
            }
            dataset.save_image_metadata(
                metadata_key="brightness",
                metadata_values=metadata_values
            )

        Note:
            The metadata values are sent to the server in batches of 500 to avoid
            overwhelming the API. Each batch is processed sequentially, and
            the method logs the progress of each batch. After all batches are
            processed, the dataset's metadata key is updated accordingly.
        """
        images_endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/images/custom_metadata"
        dataset_endpoint = (
            f"/workspaces/{self.workspace_name}/datasets/{self.key}/custom_metadata"
        )

        if not re.match("^[a-zA-Z0-9]+$", metadata_key):
            raise ValueError(
                "The 'metadata_key' parameter must contain only alphanumeric characters "
                "(no spaces, underscores, or special characters)."
            )

        for metadata_value in metadata_values.values():
            if not isinstance(metadata_value, (int, float)):
                raise ValueError(
                    f"Invalid type for value {metadata_value}: currently we only support int or float."
                )

        BATCH_SIZE = 500
        params = {
            "metadata_key": metadata_key,
        }

        metadata_batches = split_dict_into_batches(metadata_values, BATCH_SIZE)
        for i, batch in enumerate(metadata_batches):
            self.client.logger.info(f"Processing batch {i + 1}/{len(metadata_batches)}")
            images_response = self.client.patch(
                images_endpoint, params=params, body=batch
            )
            self.client.logger.info(f"{images_response.get('message')}")

        dataset_response = self.client.patch(
            dataset_endpoint,
            params=params,
        )
        self.client.logger.info(f"{dataset_response.get('message')}")

    def _create_image_coco_dict(
        self,
        image_filename: str,
        annotations: List[Annotation],
        tags: Optional[List[Tag]] = None,
    ) -> Dict[str, List[Dict]]:
        images_coco_list = [{"file_name": image_filename, "id": 0, "tags": []}]
        categories_coco_list = []
        annotations_coco_list = []
        tags_coco_list = []
        tag_name_set = set()
        category_name_set = set()
        category_id_map = {}
        tag_id = 0
        next_category_id = 0

        for tag in tags or []:
            if tag.name not in tag_name_set:
                tag_name_set.add(tag.name)
                new_tag = {
                    "id": tag_id,
                    "name": tag.name,
                    "values": tag.values,
                }
                tags_coco_list.append(new_tag)
                tag_id += 1
            images_coco_list[0]["tags"].append(new_tag)

        for i, annotation in enumerate(annotations):
            annotation.id = i

            # Handle categories
            category = annotation.category
            if category.name not in category_name_set:
                category_name_set.add(category.name)
                if category.id is None:
                    category.id = next_category_id
                else:
                    next_category_id = max(next_category_id, category.id + 1)
                category_id_map[category.name] = category.id
                categories_coco_list.append(
                    {
                        "id": category.id,
                        "name": category.name,
                    }
                )
            else:
                category.id = category_id_map[category.name]

            annotations_coco_list.append(annotation.to_coco_dict(image_id=0))

            for tag in annotation.tags or []:
                if tag.name not in tag_name_set:
                    tag_name_set.add(tag.name)
                    tags_coco_list.append(
                        {
                            "id": tag_id,
                            "name": tag.name,
                            "values": tag.values,
                        }
                    )
                    tag_id += 1

        coco_dict = {
            "images": images_coco_list,
            "categories": categories_coco_list,
            "annotations": annotations_coco_list,
            "tags": tags_coco_list,
        }
        return coco_dict

    def upload_custom_embeddings(
        self,
        embedding_name: str,
        embedding_location: Union[AWSLocation, GCSLocation, AzureLocation],
        embedding_type: str = "images",
        verbose: Optional[bool] = True
    ):
        """Upload custom embeddings to the dataset for use in Embedding viewer.

        Args:
            embedding_name (str): The display name of the embeddings.
            embedding_location (dict): The location of the embeddings in cloud storage.
            embedding_type (str): The type of embeddings. At present only 'images' is supported. 'annotations'/'predictions' coming soon!
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to True.
        """

        payload = {
            "embedding_name": embedding_name,
            "embedding_location": embedding_location
        }

        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/embeddings/{embedding_type}/upload"

        if verbose:
            with Progress(
                    SpinnerColumn("aesthetic"),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
            ) as progress:
                progress.add_task(
                    description="Uploading custom embeddings...", total=None
                )
                self.client.put(endpoint, body=payload)
                self.client.logger.info(
                    f"Successfully uploaded custom embeddings to dataset '{self.key}'."
                )
        else:
            self.client.put(endpoint, body=payload)

    def upload_custom_embeddings_from_local(
        self,
        embedding_name: str,  # display name
        embedding_path: str,  # path to JSON file
        embedding_type: str = "images",
        verbose: Optional[bool] = True
    ):
        """Upload custom embeddings from a local file to the dataset.

        Args:
            embedding_name (str): The display name of the embeddings.
            embedding_path (str): The path to the custom embeddings JSON.
            embedding_type (str): The type of embeddings. At present only 'images' is supported. 'annotations'/'predictions' coming soon!
            verbose (Optional[bool], optional): If True, provides progress updates. Defaults to True.
        """

        endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/embeddings/{embedding_type}/upload"

        file = None
        try:
            if isinstance(embedding_path, str):
                embedding_path = Path(embedding_path)
                if not embedding_path.is_file():
                    raise FileNotFoundError(
                        f"The file '{embedding_path}' does not exist."
                    )
                file = open(embedding_path, "rb")
                files = {
                    "file": file,
                }
                data = {
                    "embedding_name": embedding_name,  # the embedding name as form data
                }
            else:
                raise TypeError(
                    "embedding_path must be file path (str)"
                )

            if verbose:
                with Progress(
                    SpinnerColumn("aesthetic"),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    progress.add_task(
                        description="Uploading custom embeddings...", total=None
                    )
                    self.client.put(endpoint, files=files, data=data)
                    self.client.logger.info(
                        f"Successfully uploaded custom embeddings to dataset '{self.key}'."
                    )
            else:
                self.client.put(endpoint, files=files, data=data)
        finally:
            if file:
                file.close()


    def upload_videos_from_cloud_and_ingest(
        self,
        video_folder_location: Union[AWSLocation, GCSLocation, AzureLocation],
        sample_rate_per_second: int,
        frames_to_subsample: int,
        prompts: List[str] = ["objects"],
        threshold: float = 0.005,
    ):
        """
        Create a new dataset in the current workspace.

        Args:
            video_folder_location (Union[AWSLocation, GCSLocation, AzureLocation]): 
                The location of the folder of videos where the 
                images uploaded to the dataset come from
            sample_rate_per_second (int)
                The numbers of frames from the video to sample and save per second
            frames_to_subsample (int)
                The number of frames to subsample from all frames taken from the videos
            prompts (List[str])
                The prompts to use for the zero-shot object detection model
            threshold (float)
                The threshold the zero-shot model uses to determine what should be
                detected as an object
            
        """
        upload_video_locations_endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/videos"
        upload_video_locations_payload = {
            "video_folder_location": video_folder_location.model_dump(),
            "sample_rate_per_second": sample_rate_per_second,
            "frames_to_subsample": frames_to_subsample,
            "prompts": prompts,
            "threshold": threshold,
        }

        self.client.post(
            upload_video_locations_endpoint, 
            body=upload_video_locations_payload
        )

    def search_video(
        self,
        n_videos: Optional[int] = 50,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
        model_key: Optional[str] = None,
    ) -> List[VideoClip]:
        """Perform video search in the dataset based on filters.

        Args:
            n_videos (Optional[str], optional): Number of video clips to return. Defaults to 50.
            filter (Optional[str], optional): Filter conditions for the search. Defaults to None.
            sort_by (Optional[str], optional): Sort criteria for the search. Defaults to None.
            model_key (Optional[str], optional): Model key to filter videos. Defaults to None.

        Returns:
            List[VideoClip]: A list of video clips that match the search criteria.
        """
        video_clips = []
        page_size = n_videos if n_videos != -1 else 50
        video_clip_generator = self.video_clip_generator(
            filter=filter, sort_by=sort_by, model_key=model_key, page_size=page_size
        )
        for video_clip in video_clip_generator:
            video_clips.append(video_clip)
            if n_videos != -1 and len(video_clips) >= n_videos:
                break
        return video_clips

    def video_clip_generator(
        self,
        filter: Optional[str] = None,
        sort_by: Optional[str] = None,
        model_key: Optional[str] = None,
        page_size: Optional[int] = 50,
    ) -> Generator:
        """Generator to retrieve video clips from the dataset in a paginated manner.

        Args:
            filter (Optional[str], optional): Filter conditions for the search. Defaults to None.
            sort_by (Optional[str], optional): Sort criteria for the search. Defaults to None.
            model_key (Optional[str], optional): Model key to filter videos. Defaults to None.
            page_size (Optional[int], optional): Number of images per page. Defaults to 50.

        Yields:
            Generator: A generator yielding images.
        """
        page_number = 0

        if model_key:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/model_inferences/{model_key}/search_videos"
        else:
            endpoint = f"/workspaces/{self.workspace_name}/datasets/{self.key}/search_videos"
        while True:
            params = {
                "filter_by": filter,
                "sort_by": sort_by,
                "page": page_number,
                "size": page_size,
            }
            video_search_response = self.client.get(endpoint, params=params)
            video_clips = video_search_response.get("data", [])

            if not video_clips:
                break  # No more images to fetch, exit the loop

            for video_clip in video_clips:
                yield VideoClip.from_video_response(
                    video_clip
                )

            page_number += 1