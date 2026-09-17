from fastapi import APIRouter, UploadFile, File, Depends
from schemas.document import DocumentResponse, SearchResponse, SearchRequest
from services.document_analyser_service import DocumentAnalyserService

router = APIRouter(prefix="/document_analyser", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    service: DocumentAnalyserService = Depends(DocumentAnalyserService)
):
    return service.process_upload(file)

@router.post("/search", response_model=SearchResponse)
def search_document(
    payload: SearchRequest,
    service: DocumentAnalyserService = Depends(DocumentAnalyserService)
):
    chunks = [c.model_dump() for c in payload.chunks]
    return service.search(chunks, payload.query)