from typing import Iterator, Optional

from pptx import Presentation
from pptx.shapes.picture import Picture
from unstructured.documents.elements import Element
from unstructured.partition.pptx import AbstractPicturePartitioner, PptxPartitionerOptions
from unstructured.utils import lazyproperty

from unstructured_expanded.tools import extract_desc, create_image


class PptxExpandedPartitionerOptions(PptxPartitionerOptions):

    @lazyproperty
    def document(self) -> Presentation:
        """The python-pptx `Presentation` object loaded from the provided source file."""
        return Presentation(self.pptx_file)


class PptxPicturePartitioner(AbstractPicturePartitioner):
    namespaces: dict[str, str] = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        "p": 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    # noinspection PyProtocol
    @classmethod
    def iter_elements(
            cls,
            picture: Picture,
            opts: PptxExpandedPartitionerOptions
    ) -> Iterator[Element]:
        # noinspection PyProtectedMember
        blips = picture._element.findall('.//a:blip', namespaces=cls.namespaces)
        min_id = 0

        for blip in blips:
            # Extract relationships
            r_id = blip.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed']
            slide_id = cls.find_slide_idx(opts, r_id, min_id)
            min_id = slide_id

            # Get the image mimetype
            image_mimetype = opts.document.slides[slide_id].part.related_parts[r_id].content_type

            # Yield an image with the blob and descriptive text word generates
            yield create_image(
                image_bytes=picture.image.blob,
                desc=extract_desc(blip, base_tag="p", namespaces=cls.namespaces),
                image_mimetype=image_mimetype
            )

    @classmethod
    def find_slide_idx(cls, opts: PptxExpandedPartitionerOptions, r_id: str, min_id: int) -> Optional[int]:
        """
        Because rels are split per-slide in pptx, we need to O(n) search for the slide index that contains the image.

        :param opts: The partitioner options
        :param r_id: The relationship id of the image
        :param min_id: The minimum slide index to search from
        :return: The slide index that contains the image

        """

        for idx, slide in enumerate(opts.document.slides):

            if idx < min_id:
                continue

            for part in slide.part.rels:
                if part == r_id:
                    return idx

        raise ValueError(f"Could not find slide index for relationship id: {r_id}. This should not be possible!")
