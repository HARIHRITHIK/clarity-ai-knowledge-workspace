"""
Unit tests for multi-format document processors.
Tests PDF, DOCX, TXT, and CSV text extraction and error boundaries.
"""

import pytest
from pathlib import Path
from processors.base import get_processor
from processors.pdf_processor import PDFProcessor
from processors.docx_processor import DOCXProcessor
from processors.text_processor import TextProcessor

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_processor_factory():
    """Verify Abstract Factory returns correct processor instances."""
    assert isinstance(get_processor("pdf"), PDFProcessor)
    assert isinstance(get_processor("docx"), DOCXProcessor)
    assert isinstance(get_processor("txt"), TextProcessor)
    assert isinstance(get_processor("csv"), TextProcessor)
    
    with pytest.raises(ValueError):
        get_processor("unknown_ext")


def test_txt_processor():
    """Test text processor extracts clean string content."""
    processor = TextProcessor()
    sample_file = SAMPLE_DIR / "project_notes.txt"
    raw_bytes = sample_file.read_bytes()
    text = processor.extract_text(sample_file.name, raw_bytes)
    
    assert len(text) > 50
    assert "ACME CORPORATION" in text
    assert "David Kim" in text


def test_csv_processor():
    """Test CSV parsing formats tabular rows into readable text."""
    processor = TextProcessor()
    sample_file = SAMPLE_DIR / "sales_summary.csv"
    raw_bytes = sample_file.read_bytes()
    text = processor.extract_text(sample_file.name, raw_bytes)
    
    assert "Meridian Financial Group" in text
    assert "Enterprise SaaS" in text


def test_docx_processor():
    """Test DOCX processor extracts paragraphs and headings."""
    processor = DOCXProcessor()
    sample_file = SAMPLE_DIR / "employee_policy.docx"
    raw_bytes = sample_file.read_bytes()
    text = processor.extract_text(sample_file.name, raw_bytes)
    
    assert "Acme Corporation" in text
    assert "Paid Time Off" in text or "PTO" in text or "stipend" in text.lower()


def test_pdf_processor():
    """Test PDF processor extracts pages and structured text."""
    processor = PDFProcessor()
    sample_file = SAMPLE_DIR / "company_report.pdf"
    raw_bytes = sample_file.read_bytes()
    text = processor.extract_text(sample_file.name, raw_bytes)
    
    assert "Acme Corporation" in text
    assert "Financial" in text or "Report" in text


def test_corrupt_file_handling():
    """Ensure processors return safe output or empty string without unhandled crashes."""
    pdf_proc = PDFProcessor()
    corrupt_pdf_text = pdf_proc.extract_text("corrupt.pdf", b"NOT_A_VALID_PDF_HEADER")
    assert isinstance(corrupt_pdf_text, str)
    assert len(corrupt_pdf_text) == 0

    docx_proc = DOCXProcessor()
    corrupt_docx_text = docx_proc.extract_text("corrupt.docx", b"NOT_A_ZIP_CONTAINER")
    assert isinstance(corrupt_docx_text, str)
    assert len(corrupt_docx_text) == 0
