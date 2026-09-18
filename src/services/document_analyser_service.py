from pathlib import Path
from fastapi import Depends, UploadFile, HTTPException
import shutil, uuid
from .document_analyser.analyser import DocumentAnalyser
from .document_analyser.search import search_chunks
from .document_analyser.highlighter import render_page_with_highlight
from.document_analyser.exceptions import UnsupportedFormatError

class DocumentAnalyserService:
    UPLOAD_DIR = Path("uploads")

    def __init__(
        self,
        analyser: DocumentAnalyser = Depends(DocumentAnalyser)
    ):
        self.analyser = analyser
        self.UPLOAD_DIR.mkdir(exist_ok=True)

    def process_upload(self, file: UploadFile) -> dict:
        path = self.UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        print(path)
        try:
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            return self.analyser.analyse(str(path))
        except UnsupportedFormatError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            path.unlink(missing_ok=True)

        
    def search(self, chunks: list[dict], query: str) -> dict:
        return {
            "query": query,
            "results": search_chunks(chunks, query),
        }

    def render_highlighted_page(self, file: UploadFile, page_num: int, query: str, context_chunks: list[dict]) -> tuple[bytes, int]:
        path = self.UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        try:
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            return render_page_with_highlight(str(path), page_num, query, context_chunks)
        finally:
            path.unlink(missing_ok=True)