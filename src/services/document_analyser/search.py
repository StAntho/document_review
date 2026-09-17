import unicodedata

TITLE_TYPES = {"title", "subtitle", "heading"}


def _standardize(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.casefold()


def search_chunks(chunks: list[dict], query: str, max_following: int = 5, window: int = 1) -> list[dict]:
    norm_query = _standardize(query)
    if not norm_query:
        return []

    results = []
    for i, chunk in enumerate(chunks):
        if norm_query not in _standardize(chunk["content"]):
            continue

        ctype = chunk["type"]

        if ctype == "table":
            idxs = {i}
            context_type = "table"

        elif ctype in TITLE_TYPES:
            idxs = {i}
            for j in range(i + 1, len(chunks)):
                nxt = chunks[j]
                if nxt["page"] != chunk["page"]:
                    break
                if nxt["type"] in TITLE_TYPES and nxt["level"] <= chunk["level"]:
                    break
                idxs.add(j)
                if len(idxs) - 1 >= max_following:
                    break
            context_type = "section"

        else:
            idxs = {i}
            for j in range(i - 1, -1, -1):
                prev = chunks[j]
                if prev["page"] != chunk["page"]:
                    break
                idxs.add(j)
                if prev["type"] in TITLE_TYPES or i - j >= window:
                    break
            for j in range(i + 1, len(chunks)):
                nxt = chunks[j]
                if nxt["page"] != chunk["page"] or nxt["type"] in TITLE_TYPES:
                    break
                idxs.add(j)
                if j - i >= window:
                    break
            context_type = "paragraph"

        results.append({
            "match": chunk,
            "context_type": context_type,
            "context": [chunks[k] for k in sorted(idxs)],
        })

    return results
