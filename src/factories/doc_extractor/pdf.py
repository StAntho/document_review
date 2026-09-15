import fitz
from .base import BaseExtractor, DocumentChunk

class PDFExtractor(BaseExtractor):
    def extract(self, path: str) -> list[DocumentChunk]:
        doc = fitz.open(path)
        chunks = []
        scanned_pages = []

        for page_num, page in enumerate(doc):
            page_chunks = self._extract_text_blocks(page, page_num)
            chunks.extend(page_chunks)
            if not page_chunks:
                scanned_pages.append(page_num)

            for table in page.find_tables():
                chunks.append(DocumentChunk(
                    content = str(table.to_pandas().to_dict()),
                    type = "table",
                    page = page_num,
                ))

        chunks.sort(key=lambda c: c.page)
        return chunks

    def _extract_text_blocks(self, page, page_num: int) -> list[DocumentChunk]:
        chunks = []
        for block in page.get_text("dict")["blocks"]:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        chunks.append(DocumentChunk(
                            content = text,
                            type = self._detect_type(span),
                            level = self._detect_level(span),
                            page = page_num,
                            metadata = {
                                "font": span["font"],
                                "size": span["size"],
                                "bold": "Bold" in span["font"],
                            }
                        ))
        return chunks

    def _detect_type(self, span: dict) -> str:
        if span["size"] > 18: return "title"
        if span["size"] > 14: return "subtitle"
        if "Bold" in span["font"]: return "heading"
        return "paragraph"

    def _detect_level(self, span: dict) -> str:
        if span["size"] > 18: return 1
        if span["size"] > 14: return 2
        if span["size"] > 11: return 3
        return 0
