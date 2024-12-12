from typing import IO, Any
from xml.dom.minidom import Element

from unstructured.chunking import add_chunking_strategy
from unstructured.file_utils.model import FileType
from unstructured.partition.common.metadata import apply_metadata
from unstructured.partition.docx import DocxPartitionerOptions, _DocxPartitioner

from .partition_picture import DocxPicturePartitioner


@apply_metadata(FileType.DOCX)
@add_chunking_strategy
def partition_docx(
        filename: str | None = None,
        *,
        file: IO[bytes] | None = None,
        include_page_breaks: bool = True,
        infer_table_structure: bool = True,
        starting_page_number: int = 1,
        strategy: str | None = None,
        **_: Any,
) -> list[Element]:
    opts = DocxPartitionerOptions.load(
        file=file,
        file_path=filename,
        include_page_breaks=include_page_breaks,
        infer_table_structure=infer_table_structure,
        starting_page_number=starting_page_number,
        strategy=strategy,
    )

    opts.register_picture_partitioner(DocxPicturePartitioner)
    elements = _DocxPartitioner.iter_document_elements(opts)

    return list(elements)
