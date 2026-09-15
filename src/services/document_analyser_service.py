from pathlib import Path
from fastapi import Depends, UploadFile, HTTPException
import shutil, uuid
from .document_analyser.analyser import DocumentAnalyser

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
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            path.unlink(missing_ok=True)