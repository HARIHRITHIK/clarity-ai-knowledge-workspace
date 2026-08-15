"""
Abstract base class for all document processors.
Adding support for a new file format requires only:
  1. Create a new file in processors/
  2. Subclass BaseProcessor and implement extract_text()
  3. Register it in the factory below
Nothing else in the application changes.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseProcessor(ABC):
    """Contract every processor must fulfil."""

    @abstractmethod
    def extract_text(self, file_path: str, raw_bytes: bytes) -> str:
        """
        Extract plain text from the given source.

        Args:
            file_path: Original filename (used to detect format and for error messages)
            raw_bytes: Raw file bytes (used when reading from UploadedFile)

        Returns:
            Extracted plain text. Empty string on failure — never raises.
        """

    def clean(self, text: str) -> str:
        """
        Basic post-processing applied to every extracted text.
        Removes null bytes, normalises whitespace.
        """
        if not text:
            return ""
        text = text.replace("\x00", "")
        lines = [line.strip() for line in text.splitlines()]
        # Collapse runs of more than 2 blank lines
        cleaned, blanks = [], 0
        for line in lines:
            if line == "":
                blanks += 1
                if blanks <= 2:
                    cleaned.append(line)
            else:
                blanks = 0
                cleaned.append(line)
        return "\n".join(cleaned).strip()


# ── Processor Factory ─────────────────────────────────────────────────────────

def get_processor(extension: str) -> BaseProcessor:
    """Return the correct processor for a given file extension."""
    # Import here to avoid circular imports at module load
    from processors.pdf_processor  import PDFProcessor
    from processors.docx_processor import DOCXProcessor
    from processors.text_processor import TextProcessor

    registry = {
        "pdf":  PDFProcessor,
        "docx": DOCXProcessor,
        "txt":  TextProcessor,
        "csv":  TextProcessor,
    }
    cls = registry.get(extension.lower())
    if cls is None:
        raise ValueError(f"Unsupported file extension: .{extension}")
    return cls()
