from fastapi import APIRouter, UploadFile, File, Depends, Form
from schemas.document import DocumentResponse, SearchResponse, SearchRequest, HighlightResponse
from services.document_analyser_service import DocumentAnalyserService
import json, base64

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

@router.post("/highlight", response_model=HighlightResponse)
def highlight_page(
    file: UploadFile = File(...),
    page_num: int = Form(...),
    query: str = Form(...),
    chunks: str = Form(...),
    service: DocumentAnalyserService = Depends(DocumentAnalyserService)
):
    context_chunks = json.loads(chunks)
    img_bytes, nb_hits = service.render_highlighted_page(file, page_num, query, context_chunks)
    return {"image_base64": base64.b64encode(img_bytes).decode(), "nb_hits": nb_hits}