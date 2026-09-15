from factories.doc_extractor.base import DocumentChunk

def normalize(chunks: list[DocumentChunk]) -> list[dict]:
    return [
        {
            "content": c.content,
            "type": c.type,
            "level": c.level,
            "page": c.page,
            "metadata": c.metadata,
        }
        for c in chunks
        if c.content.strip()
    ]