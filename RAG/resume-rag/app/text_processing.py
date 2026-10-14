import re


def normalize_text(text: str) -> str:
    """Remove noisy whitespace while preserving paragraph boundaries."""
    text = text.replace("\x00", "")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]

    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs).strip()


def chunk_text(
    text: str,
    chunk_size_words: int = 180,
    overlap_words: int = 30,
) -> list[str]:
    """Split text into overlapping word windows for simple local retrieval."""
    if chunk_size_words <= 0:
        raise ValueError("chunk_size_words must be positive")
    if overlap_words < 0 or overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be between 0 and chunk size")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    step = chunk_size_words - overlap_words
    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size_words]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size_words >= len(words):
            break
    return chunks
