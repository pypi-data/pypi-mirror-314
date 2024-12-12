from typing import IO, Any

from unstructured.chunking import add_chunking_strategy
from unstructured.documents.elements import Element
from unstructured.file_utils.model import FileType
from unstructured.partition.common.metadata import apply_metadata
from unstructured.partition.pptx import _PptxPartitioner
from unstructured.partition.utils.constants import PartitionStrategy

from unstructured_expanded.partition.pptx.partition_picture import PptxPicturePartitioner, PptxExpandedPartitionerOptions


@apply_metadata(FileType.PPTX)
@add_chunking_strategy
def partition_pptx(
        filename: str | None = None,
        *,
        file: IO[bytes] | None = None,
        include_page_breaks: bool = True,
        include_slide_notes: bool | None = None,
        infer_table_structure: bool = True,
        starting_page_number: int = 1,
        strategy: str = PartitionStrategy.FAST,
        **_: Any,
) -> list[Element]:

    opts = PptxExpandedPartitionerOptions(
        file=file,
        file_path=filename,
        include_page_breaks=include_page_breaks,
        include_slide_notes=include_slide_notes,
        infer_table_structure=infer_table_structure,
        strategy=strategy,
        starting_page_number=starting_page_number,
    )

    opts.register_picture_partitioner(PptxPicturePartitioner)
    return list(_PptxPartitioner.iter_presentation_elements(opts))