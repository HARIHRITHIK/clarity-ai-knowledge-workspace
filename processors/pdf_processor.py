"""PDF processor — extracts plain text from PDF files using pypdf."""

import io
from processors.base import BaseProcessor


class PDFProcessor(BaseProcessor):
    """Extracts text from PDF files. Falls back gracefully on encrypted or malformed PDFs."""

    def extract_text(self, file_path: str, raw_bytes: bytes) -> str:
        try:
            from pypdf import PdfReader
        except ImportError:
            return f"[pypdf not installed — cannot parse {file_path}]"

        try:
            reader = PdfReader(io.BytesIO(raw_bytes))
            pages = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
            raw = "\n\n".join(pages)
            return self.clean(raw)
        except Exception as exc:
            # Return empty string so the pipeline can still record an error
            # without crashing
            return ""
