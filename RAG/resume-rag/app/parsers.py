from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.text_processing import normalize_text


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text(filename: str, content: bytes) -> str:
    """Extract plain text from a supported resume format."""
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Supported file types are PDF, DOCX, and TXT")

    if extension == ".pdf":
        reader = PdfReader(BytesIO(content))
        raw_text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    elif extension == ".docx":
        document = Document(BytesIO(content))
        raw_text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    else:
        try:
            raw_text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("TXT files must use UTF-8 encoding") from error

    text = normalize_text(raw_text)
    if not text:
        raise ValueError(
            "No readable text was found. Scanned PDFs need OCR, which is not enabled."
        )
    return text
