import pytest

from app.parsers import extract_text


def test_extracts_utf8_text_resume() -> None:
    assert extract_text("resume.txt", b"Python\n\nFastAPI") == "Python\n\nFastAPI"


def test_rejects_unknown_file_type() -> None:
    with pytest.raises(ValueError, match="Supported file types"):
        extract_text("resume.exe", b"content")
