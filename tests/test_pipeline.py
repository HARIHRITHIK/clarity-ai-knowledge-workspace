"""
Unit tests for the end-to-end processing pipeline orchestrator.
Tests progressive document hydration and error handling.
"""

from pathlib import Path
from core.pipeline import Pipeline
from core.document import Document
import config

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_pipeline_txt_execution():
    """Test full 5-stage pipeline on text document."""
    pipeline = Pipeline()
    progress_stages = []

    def on_progress(stage, pct):
        progress_stages.append((stage, pct))

    sample_file = SAMPLE_DIR / "project_notes.txt"
    doc = pipeline.run_from_path(str(sample_file))

    assert doc.is_processed is True
    assert doc.has_error is False
    assert len(doc.summary) > 0
    assert len(doc.key_facts) > 0
    assert doc.word_count > 20
    assert doc.category in config.CATEGORY_KEYWORDS.keys() or doc.category == "General"


def test_pipeline_pdf_execution():
    """Test full 5-stage pipeline on PDF document."""
    pipeline = Pipeline()
    sample_file = SAMPLE_DIR / "company_report.pdf"
    
    doc = pipeline.run_from_path(str(sample_file))
    assert doc.is_processed is True
    assert doc.has_error is False
    assert doc.category in config.CATEGORY_KEYWORDS.keys()
    assert len(doc.summary) > 0


def test_pipeline_missing_file_handling():
    """Verify missing files are handled gracefully with clear error state."""
    pipeline = Pipeline()
    doc = pipeline.run_from_path("non_existent_document_file.pdf")
    
    assert doc.has_error is True
    assert "File not found" in (doc.processing_error or "")
