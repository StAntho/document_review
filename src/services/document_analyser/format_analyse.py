import mimetypes

MIME_TO_FORMAT = {
    "application/pdf": "pdf"
}

def analysing_format(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return MIME_TO_FORMAT.get(mime, "unknown")