from pydantic import BaseModel

class DocumentResponse(BaseModel):
    path: str
    format: str
    structure: dict
    chunks: list[ChunkResponse]
    markdown_path: str | None = None
    
class ChunkResponse(BaseModel):
    content: str
    type: str
    level: int
    page: int
    metadata: dict