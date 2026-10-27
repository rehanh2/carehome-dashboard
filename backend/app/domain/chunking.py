def split_into_chunks(text: str, max_words: int = 60, overlap: int = 10) -> list[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text.strip()]

    chunks = []
    step = max_words - overlap
    for start in range(0, len(words), step):
        chunk = words[start:start + max_words]
        chunks.append(" ".join(chunk))
        if start + max_words >= len(words):
            break
    return chunks