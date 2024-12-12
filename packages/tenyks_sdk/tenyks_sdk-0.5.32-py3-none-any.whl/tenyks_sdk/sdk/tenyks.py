from typing import List, Optional, Union

from requests.exceptions import HTTPError

from tenyks_sdk.sdk.client import Client
from tenyks_sdk.sdk.cloud import AWSLocation, AzureLocation, GCSLocation
from tenyks_sdk.sdk.dataset.dataset import Dataset
from tenyks_sdk.sdk.exceptions import ClientError
from tenyks_sdk.sdk.workspace import Workspace


class Tenyks:

    def __init__(
        self,
        client: Client,
        workspace_name: Optional[str] = None,
    ):
        self.client = client
        self.set_workspace(workspace_name, verbose=False)

    @classmethod
    def authenticate_with_api_key(
        cls,
        api_base_url: str,
        api_key: str,
        api_secret: str,
        workspace_name: str,
    ):
        """
        Authenticate using an API key.

        Args:
            api_base_url (str): The base URL of the Tenyks API.
            api_key (str): The API key provided for authentication.
            api_secret (str): The API secret corresponding to the API key.
            workspace_name (str): The name of the workspace to use after authentication.

        Raises:
            ClientError: If authentication fails due to invalid or expired credentials.
            e: Other HTTP errors raised during the request.

        Returns:
            Tenyks: An instance of the Tenyks class.
        """
        try:
            client = Client.authenticate_with_api_key(api_base_url, api_key, api_secret)
            client.logger.info("Successfully authenticated to the Tenyks API.")
            return cls(client, workspace_name)
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ClientError(
                    "Failed to authenticate to the Tenyks API. Credentials are invalid or expired."
                )
            else:
                raise e

    @classmethod
    def authenticate_with_login(
        cls,
        api_base_url: str,
        username: str,
        password: str,
        workspace_name: str,
    ):
        """
        Authenticate using a username and password.

        Args:
            api_base_url (str): The base URL of the Tenyks API.
            username (str): The username for authentication.
            password (str): The password for authentication.
            workspace_name (str): The name of the workspace to use after authentication.

        Raises:
            ClientError: If authentication fails due to invalid credentials.
            e: Other HTTP errors raised during the request.

        Returns:
            Tenyks: An instance of the Tenyks class.
        """
        try:
            client = Client.authenticate_with_login(api_base_url, username, password)
            client.logger.info("Successfully authenticated to the Tenyks API.")
            return cls(client, workspace_name)
        except HTTPError as e:
            if e.response.status_code == 401:
                raise ClientError(
                    "Failed to authenticate to the Tenyks API. Credentials are invalid."
                )
            else:
                raise e

    def set_workspace(self, workspace_key: str, verbose: Optional[bool] = True) -> None:
        """
        Set the active workspace.

        Args:
            workspace_key (str): The key of the workspace to set as active.
            verbose (Optional[bool], optional): Whether to log the change of workspace. Defaults to True.

        Raises:
            ValueError: If the workspace name is empty or the workspace does not exist.
        """
        if not workspace_key:
            raise ValueError("Workspace name cannot be empty.")

        workspaces = self.get_workspaces()

        # Check if the provided workspace_name is in the list of workspaces
        matching_workspace = None
        for workspace in workspaces:
            if workspace.key == workspace_key:
                matching_workspace = workspace
                break

        if matching_workspace:
            self.workspace_name = matching_workspace.key
            if verbose:
                self.client.logger.info(f"Workspace set to '{workspace_key}'.")
        else:
            raise ValueError(
                f"Workspace '{workspace_key}' is not accessible or does not exist."
            )

    def get_datasets(self) -> List[Dataset]:
        """
        Retrieve a list of datasets in the current workspace.

        Returns:
            List[Dataset]: A list of Dataset objects available in the workspace.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets"
        datasets_response = self.client.get(endpoint)
        return [
            Dataset.from_dataset_response(
                {**dataset}, client=self.client, workspace_name=self.workspace_name
            )
            for dataset in datasets_response
        ]

    def get_dataset_names(self) -> List[str]:
        """
        Retrieve the names of datasets in the current workspace.

        Returns:
            List[str]: A list of dataset names available in the workspace.
        """
        datasets = self.get_datasets()
        return [dataset.name for dataset in datasets]

    def get_dataset(self, key: str) -> Dataset:
        """
        Retrieve a specific dataset by its key.

        Args:
            key (str): The key of the dataset to retrieve.

        Returns:
            Dataset: The Dataset object corresponding to the specified key.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{key}"
        dataset_response = self.client.get(endpoint)
        return Dataset.from_dataset_response(
            {**dataset_response}, client=self.client, workspace_name=self.workspace_name
        )

    def create_dataset(
        self,
        name: str,
        images_location: Optional[
            Union[AWSLocation, GCSLocation, AzureLocation]
        ] = None,
        metadata_location: Optional[
            Union[AWSLocation, GCSLocation, AzureLocation]
        ] = None,
    ) -> Dataset:
        """
        Create a new dataset in the current workspace.

        Args:
            name (str): The name of the new dataset.
            images_location (Optional[Union[AWSLocation, GCSLocation, AzureLocation]], optional):
                The location of the dataset's images. Defaults to None.
            metadata_location (Optional[Union[AWSLocation, GCSLocation, AzureLocation]], optional):
                The location of the dataset's metadata. Defaults to None.

        Returns:
            Dataset: The created Dataset object.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets"
        payload = {
            "key": name.lower(),
            "display_name": name,
        }

        if images_location:
            payload["images_location"] = images_location.model_dump()
        if metadata_location:
            payload["metadata_location"] = metadata_location.model_dump()

        dataset_response = self.client.post(endpoint, body=payload)
        dataset = Dataset.from_dataset_response(
            {**dataset_response}, client=self.client, workspace_name=self.workspace_name
        )
        self.client.logger.info(
            f"Dataset '{name}' created successfully with key {dataset.key}."
        )
        return dataset

    def delete_dataset(self, key: str) -> None:
        """
        Delete a dataset by its key.

        Args:
            key (str): The key of the dataset to delete.
        """
        endpoint = f"/workspaces/{self.workspace_name}/datasets/{key}"
        self.client.delete(endpoint)
        self.client.logger.info(f"Dataset {key} deleted successfully.")

    def get_workspaces(self, page: int = 1, page_size: int = 10) -> List[Workspace]:
        """
        Retrieve a list of workspaces accessible to the user.

        Args:
            page (int, optional): The page number for paginated results. Defaults to 1.
            page_size (int, optional): The number of workspaces to retrieve per page. Defaults to 10.

        Returns:
            List[Workspace]: A list of Workspace objects accessible to the user.
        """
        endpoint = "/workspaces"
        params = {"page": page, "page_size": page_size}
        workspaces_response = self.client.get(endpoint, params=params)
        workspaces_list = workspaces_response.get("data")
        return [Workspace(self.client, **workspace) for workspace in workspaces_list]

    def get_workspace(self, id: str) -> Workspace:
        """
        Retrieve a specific workspace by its ID.

        Args:
            id (str): The ID of the workspace to retrieve.

        Returns:
            Workspace: The Workspace object corresponding to the specified ID.
        """
        endpoint = f"/workspaces/{id}"
        workspace_response = self.client.get(endpoint)
        return Workspace(self.client, **workspace_response)

    def create_workspace(self, name: str) -> Workspace:
        """
        Create a new workspace.

        Args:
            name (str): The name of the new workspace.

        Returns:
            Workspace: The created Workspace object.
        """
        endpoint = "/workspaces"
        payload = {"name": name}
        workspace_response = self.client.post(endpoint, body=payload)
        return Workspace(self.client, **workspace_response)
