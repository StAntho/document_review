from pathlib import Path
from fastapi import HTTPException
from schemas.document import DocumentResponse, ChunkResponse
from .format_analyse import analysing_format
from factories.doc_extractor import EXTRACTORS
from .normalizer import normalize
from .exceptions import UnsupportedFormatError

class DocumentAnalyser:
    def analyse(self, path: str) -> dict:
        fmt = analysing_format(path)
        extractor = EXTRACTORS.get(fmt)

        if not extractor:
            raise UnsupportedFormatError(fmt)

        chunks = extractor().extract(path)
        structure = {}
        normalized_chunks = normalize(chunks)

        markdown_path = None

        return {
            "path": path,
            "format": fmt,
            "structure": structure,
            "chunks": [ChunkResponse(**c) for c in normalized_chunks],
            "markdown_path": markdown_path,
        }
