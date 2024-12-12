import base64
import sys
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import List, Optional

import requests
from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

from tenyks_sdk.sdk.image import Image


def display_images(
    images: List[Image],
    n_images_to_show: Optional[int] = None,
    draw_bboxes: Optional[bool] = False,
    n_cols: Optional[int] = 3,
) -> None:
    """
    Utility function to display Tenyks Images

    Args:
        images (List[Image]): A list of `Image` objects to be displayed.
        n_images_to_show (Optional[int], optional): The number of images to display.
            If `None`, all images will be shown. Defaults to `None`.
        draw_bboxes (Optional[bool], optional): Whether to draw bounding boxes around annotations.
            If `True`, bounding boxes will be drawn based on image annotations. Defaults to `False`.
        n_cols (Optional[int], optional): The number of columns in the display grid.
            The layout will adjust the number of rows accordingly. Defaults to `3`.

    Raises:
        RuntimeError: If an error occurs while displaying the images, such as an invalid image format or a missing file.
    """
    # Check if the code is running in an IPython environment
    if "ipykernel" not in sys.modules:
        raise RuntimeError(
            "This function is intended to be used within a Jupyter Notebook only."
        )

    from IPython.display import HTML, display

    images = images[:n_images_to_show] if n_images_to_show else images

    with ThreadPoolExecutor() as executor:
        results = list(
            executor.map(lambda img: process_image(img, draw_bboxes), images)
        )

    images_html = "<table><tr>"
    for index, data_uri in enumerate(results):
        if index > 0 and index % n_cols == 0:
            images_html += "</tr><tr>"

        images_html += (
            f'<td style="padding:10px"><img src="{data_uri}" style="width:100%"></td>'
        )
    images_html += "</tr></table>"
    display(HTML(images_html))


def process_image(image: Image, draw_bboxes: bool) -> str:
    img = fetch_image(image)
    if draw_bboxes:
        img = fetch_and_draw_bounding_boxes(img, image)
    return pil_image_to_data_uri(img)


def fetch_image(image: Image) -> PILImage:
    response = requests.get(image.raw_image_url, stream=True)
    img = PILImage.open(BytesIO(response.content))
    return img


def fetch_and_draw_bounding_boxes(img: PILImage, image: Image) -> PILImage:

    def draw_boxes(draw, bbox, label, color, dashed=False, score=None):
        x, y, w, h = bbox
        xyxy = [x, y, x + w, y + h]

        if dashed:
            draw_dashed_rectangle(draw, xyxy, fill=color, width=3)
        else:
            draw.rectangle(xyxy, outline=color, width=3)

        # Draw the label at the top for annotations and bottom for predictions
        full_label = f"{label} ({score:.2f})" if score is not None else label
        text_size = draw.textbbox((0, 0), full_label, font=font)
        text_width, text_height = (
            text_size[2] - text_size[0],
            text_size[3] - text_size[1],
        )
        padding = 2

        if score is not None:  # Prediction
            text_background = [
                x,
                y + h,
                x + text_width + padding,
                y + h + text_height + padding + 2,
            ]
            text_position = (x + padding, y + h + padding)
        else:  # Annotation
            text_background = [
                x,
                y - text_height - padding - 2,
                x + text_width + padding,
                y,
            ]
            text_position = (x + padding, y - text_height - padding - 2)

        draw.rectangle(text_background, fill=color)
        draw.text(text_position, full_label, fill="white", font=font)

    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Draw the bounding boxes and labels for annotations
    for annotation in image.annotations:
        draw_boxes(
            draw,
            annotation.coordinates,
            annotation.category.name,
            annotation.category.color,
        )

    # Draw the bounding boxes and labels for predictions
    for prediction in image.predictions:
        draw_boxes(
            draw,
            prediction.coordinates,
            prediction.category.name,
            prediction.category.color,
            dashed=True,
            score=prediction.score,
        )

    return img


def pil_image_to_data_uri(img: PILImage) -> str:
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=50)  # Save as JPEG to reduce size
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_str}"


def draw_dashed_rectangle(draw, xy, dash_length=5, **kwargs):
    x1, y1, x2, y2 = map(int, xy)
    for i in range(x1, x2, dash_length * 2):
        draw.line([(i, y1), (i + dash_length, y1)], **kwargs)
        draw.line([(i, y2), (i + dash_length, y2)], **kwargs)
    for i in range(y1, y2, dash_length * 2):
        draw.line([(x1, i), (x1, i + dash_length)], **kwargs)
        draw.line([(x2, i), (x2, i + dash_length)], **kwargs)
