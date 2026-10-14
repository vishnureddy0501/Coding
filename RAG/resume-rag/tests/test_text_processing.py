from app.text_processing import chunk_text, normalize_text


def test_normalize_text_preserves_paragraphs() -> None:
    text = "  Python   Developer  \nFastAPI\n\n  MongoDB  "
    assert normalize_text(text) == "Python Developer FastAPI\n\nMongoDB"


def test_chunk_text_adds_overlap() -> None:
    chunks = chunk_text("one two three four five six", chunk_size_words=4, overlap_words=2)
    assert chunks == ["one two three four", "three four five six"]


def test_chunk_text_handles_empty_text() -> None:
    assert chunk_text("") == []
