"""DOCX processor — extracts plain text from Word documents using python-docx."""

import io
from processors.base import BaseProcessor


class DOCXProcessor(BaseProcessor):
    """Extracts text from .docx files, preserving paragraph structure."""

    def extract_text(self, file_path: str, raw_bytes: bytes) -> str:
        try:
            from docx import Document as DocxDocument
        except ImportError:
            return f"[python-docx not installed — cannot parse {file_path}]"

        try:
            doc = DocxDocument(io.BytesIO(raw_bytes))
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            raw = "\n\n".join(paragraphs)
            return self.clean(raw)
        except Exception:
            return ""
