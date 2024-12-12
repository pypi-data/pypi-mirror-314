import os
from dataclasses import dataclass
from typing import Optional

from fastclasses_json import dataclass_json
from werkzeug.utils import secure_filename


@dataclass_json
@dataclass
class ImageKeyFile:
    image_key: str
    file_extension: str


def extract_image_key(
    file_path: str, image_key_version: Optional[str] = None
) -> ImageKeyFile:
    if image_key_version and image_key_version == "v2":
        return extract_image_key_v2(file_path)
    return extract_image_key_v1(file_path)


def remove_filename_slashes_v2(filename: str) -> str:
    return filename.replace("/", "_").replace("\\", "_").lstrip("_")


def replace_dots_v2(filename: str) -> str:
    return filename.replace(".", "_")


def create_image_key_v2(image_name: str, file_extension: str) -> str:
    return f"{image_name}_{file_extension}"


def extract_image_key_v2(file_path: str) -> ImageKeyFile:
    filename = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    secured_filename = secure_filename(filename)

    # Split the filename into name and extension
    file_name_without_ext, file_extension = os.path.splitext(secured_filename)
    image_key_extension = file_extension.lstrip(".")

    # Replace dots in the base filename
    file_name_without_ext = replace_dots_v2(file_name_without_ext)

    # Combine directory and filename to get the image name
    image_name = os.path.join(dir_name, file_name_without_ext)
    image_name = remove_filename_slashes_v2(image_name)

    # Generate the image key
    image_key = create_image_key_v2(image_name, image_key_extension)

    return ImageKeyFile(image_key, file_extension)


def remove_filename_slashes_v1(filename):
    return filename.replace("/", "_")


def get_image_key_v1(image_name):
    return remove_filename_slashes_v2(image_name)


def extract_image_key_v1(file_path) -> ImageKeyFile:
    filename = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    filename = secure_filename(filename)
    file_name_without_ext, file_extension = os.path.splitext(filename)

    image_name = os.path.join(dir_name, file_name_without_ext)
    image_key = get_image_key_v1(image_name)

    return ImageKeyFile(image_key, file_extension)
