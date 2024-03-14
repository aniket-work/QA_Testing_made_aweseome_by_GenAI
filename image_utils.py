import base64
import logging
from io import BytesIO
from PIL import Image
from constants import PNG_FORMAT, JPEG_FORMAT, IMAGE_SRC_TEMPLATE, MAX_WIDTH_STYLE

# Define logger
logger = logging.getLogger(__name__)


def convert_image_to_base64(image_file_path, image_format=PNG_FORMAT):
    """
    Convert PIL image to a Base64 encoded string.

    :param image_file_path: Path to the input image file.
    :param image_format: Optional. Output format for the image (e.g., PNG, JPEG).
    :return: Base64 encoded string representing the image.
    """
    try:
        with Image.open(image_file_path) as pil_image:
            buffered = BytesIO()
            pil_image.save(buffered, format=image_format.upper())
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    except Exception as e:
        logger.error(f"Error converting image to Base64: {str(e)}")
        return None


def display_base64_image(base64_string, image_format=JPEG_FORMAT):
    """
    Display an image represented by a Base64 encoded string.

    :param base64_string: Base64 encoded string representing the image.
    :param image_format: Optional. Format of the image (e.g., JPEG, PNG).
    :return: HTML code to display the image.
    """
    try:
        image_src = IMAGE_SRC_TEMPLATE.format(format=image_format.lower(), data=base64_string)
        image_html = f'<img src="{image_src}" style="{MAX_WIDTH_STYLE}"/>'
        return image_html
    except Exception as e:
        logger.error(f"Error displaying Base64 image: {str(e)}")
        return None
