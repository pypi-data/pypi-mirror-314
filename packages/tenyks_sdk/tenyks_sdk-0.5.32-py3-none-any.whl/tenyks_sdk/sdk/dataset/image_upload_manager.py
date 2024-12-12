from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Union

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from tenyks_sdk.sdk.client import Client


class ImageUploadManager:

    # TODO This is not ideal at all. Good example to take a look at:
    #  https://github.com/v7labs/darwin-py/blob/master/darwin/dataset/upload_manager.py#L254C24-L254C26

    def __init__(
        self,
        client: Client,
        max_workers: int = 20,
        retries_per_file: int = 3,
        valid_image_extensions: List[str] = [".jpg", ".jpeg", ".png"],
    ):
        self.client = client
        self.max_workers = max_workers
        self.retries_per_file = retries_per_file
        self.valid_image_extensions = valid_image_extensions

    def upload_files(
        self,
        file_paths_or_dir: Union[Path, List[Path]],
        upload_endpoint: str,
        verbose: Optional[bool] = True,
    ):
        if isinstance(file_paths_or_dir, Path) and file_paths_or_dir.is_dir():
            file_path_list = [
                file_path
                for file_path in file_paths_or_dir.rglob("*")  # rglob is recursive glob
                if file_path.is_file()
                and file_path.suffix in self.valid_image_extensions
            ]
        else:
            file_path_list = [
                file_path
                for file_path in file_paths_or_dir
                if file_path.is_file()
                and file_path.suffix in self.valid_image_extensions
            ]

        successes, failures = [], []

        progress_bar = Progress(
            TextColumn(
                "Uploading Images [progress.percentage]{task.percentage:>3.0f}%"
            ),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
        )

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.upload_file, path, upload_endpoint): path
                for path in file_path_list
            }
            if verbose:
                with progress_bar as p:
                    for future in p.track(
                        as_completed(future_to_file),
                        total=len(future_to_file),
                    ):
                        file_name, result = future.result()
                        if result:
                            successes.append(file_name)
                        else:
                            failures.append(file_name)
            else:
                for future in as_completed(future_to_file):
                    file_name, result = future.result()
                    if result:
                        successes.append(file_name)
                    else:
                        failures.append(file_name)
        return successes, failures

    def upload_file(self, file_path: Path, upload_endpoint: str):
        for attempt in range(self.retries_per_file):
            try:
                with open(file_path, "rb") as file:
                    files = {"file": (file_path.name, file)}
                    response = self.client.put(upload_endpoint, files=files)
                if response:
                    return (file_path.name, True)
                else:
                    self.client.logger.error(
                        f"Upload failed for {file_path.name}, attempt {attempt + 1}"
                    )
            except (
                Exception
            ) as e:  # Catch any unexpected errors that were not handled by the client
                self.client.logger.error(
                    f"Failed to upload {file_path.name} due to {e}, attempt {attempt + 1}"
                )

        return (file_path.name, False)
