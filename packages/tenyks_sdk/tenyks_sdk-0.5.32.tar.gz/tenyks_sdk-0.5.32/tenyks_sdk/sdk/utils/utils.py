from io import BytesIO

import cv2
import numpy as np
import requests


def download_image(image_url: str) -> np.ndarray:
    """Downloads an image from the given URL and returns it as a NumPy array."""
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    image = np.array(bytearray(image_data.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image
