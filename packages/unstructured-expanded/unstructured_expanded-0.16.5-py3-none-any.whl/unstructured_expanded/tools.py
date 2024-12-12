import base64
import io
from typing import Any

from PIL.Image import open as open_image
from PIL.Image import Resampling
from unstructured.documents.elements import Image, ElementMetadata


def extract_desc(
        blip: Any,
        base_tag: str,
        namespaces: dict[str, str]
) -> str:
    blip_pic = blip.getparent().getparent()
    desc: str = "No Description Available"

    nv_pic_pr = blip_pic.find(f'{base_tag}:nvPicPr', namespaces=namespaces)
    if nv_pic_pr is not None:
        c_nv_pr = nv_pic_pr.find(f'{base_tag}:cNvPr', namespaces=namespaces)
        if c_nv_pr is not None:
            desc = c_nv_pr.attrib.get("descr")
            desc = desc.replace('\n\nDescription automatically generated', '')

    return desc


def create_image(
        image_bytes: bytes,
        image_mimetype: str,
        desc: str,
) -> Image:
    image_b64: str = downscale_and_compress_image(image_bytes)

    return Image(
        text=desc,
        metadata=ElementMetadata(
            image_base64=image_b64,
            image_mime_type=image_mimetype
        )
    )


def downscale_and_compress_image(image_bytes: bytes) -> str:
    """
    Downscale and compress an image to a maximum width or height of 1024 pixels, and convert to base64

    :param image_bytes: The image bytes
    :return: Base64 encoded image

    """

    with open_image(io.BytesIO(image_bytes)) as img:

        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Get current dimensions
        width, height = img.size

        # Determine the scaling factor, keeping the aspect ratio
        if width > height:
            # Width is longer, scale based on width
            scale = 1024 / width
        else:
            # Height is longer, scale based on height
            scale = 1024 / height

        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)

        # Resize the image
        resized_img = img.resize((new_width, new_height), Resampling.LANCZOS)

        # Convert to JPEG for compression
        with io.BytesIO() as output:
            # Save image to the BytesIO object, with JPEG format and reduced quality
            resized_img.save(output, format='JPEG', quality=85)
            # Retrieve the compressed image data
            compressed_image_bytes = output.getvalue()

            # Encode to base64
            base64_encoded = base64.b64encode(compressed_image_bytes)
            # Convert bytes to string
            return base64_encoded.decode('utf-8')
