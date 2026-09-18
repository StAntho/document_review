
import fitz

def render_page_with_highlight(pdf_path: str, page_num: int, query: str, context_chunks: list = None):
    doc = fitz.open(pdf_path)
    if page_num >= len(doc):
        doc.close()
        return None, 0

    page = doc[page_num]

    rects = []
    for variant in {query, query.lower(), query.upper(), query.capitalize()}:
        rects.extend(page.search_for(variant))

    if not rects and context_chunks:
        norm_query = query.strip().lower()
        for chunk in context_chunks:
            if chunk.get("page") != page_num:
                continue
            for w in chunk.get("metadata", {}).get("words", []):
                if norm_query in w["text"].lower():
                    xmin, ymin, xmax, ymax = w["bbox"]
                    rects.append(fitz.Rect(
                        xmin * page.rect.width,
                        ymin * page.rect.height,
                        xmax * page.rect.width,
                        ymax * page.rect.height,
                    ))

    for rect in rects:
        page.draw_rect(rect, color=(1, 0.76, 0), fill=(1, 1, 0), fill_opacity=0.4, overlay=True)

    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    doc.close()
    return img_bytes, len(rects)
