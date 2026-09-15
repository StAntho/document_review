from fastapi import APIRouter, UploadFile, File, Depends
from schemas.document import DocumentResponse
from services.document_analyser_service import *
router = APIRouter(prefix="/document_analyser", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    service: DocumentAnalyserService = Depends(DocumentAnalyserService)
):
    return service.process_upload(file)
