"""
Unit tests for the HTML report exporter.
Verifies report construction, stats aggregation, and XSS/HTML escaping.
"""

from core.document import Document, Entity
from utils.exporter import generate_html_report


def test_html_report_generation():
    """Test generating a standalone HTML report with metadata."""
    doc = Document(
        id="test-doc-1",
        filename="financial_summary.pdf",
        category="Financial Report",
        summary="Company achieved $24.7 million in annual revenue with strong EBITDA.",
        key_facts=["Revenue reached $24.7 million.", "EBITDA was $4.2 million."],
        word_count=520,
        file_type="pdf",
        entities={
            "PERSON": [Entity(text="Sarah Rodriguez", label="PERSON", count=3)],
            "ORG": [Entity(text="TechSupply Solutions", label="ORG", count=2)],
            "MONEY": [Entity(text="$24.7 million", label="MONEY", count=1)],
        },
    )

    html_out = generate_html_report([doc], workspace_name="Acme Corporation")

    assert "<!DOCTYPE html>" in html_out
    assert "Acme Corporation" in html_out
    assert "Financial Summary" in html_out
    assert "$24.7 million" in html_out
    assert "Sarah Rodriguez" in html_out
    assert "TechSupply Solutions" in html_out
    assert "Document Intelligence" in html_out


def test_html_escaping_and_xss_protection():
    """Verify special characters and script tags in document data are escaped."""
    doc = Document(
        id="xss-doc",
        filename="xss_script_attack.txt",
        category="Contract / Legal",
        summary="Testing <script>alert('xss')</script> and <b>bold</b> tags.",
        key_facts=["Fact with <tag> & 'quotes'."],
        word_count=100,
        file_type="txt",
    )

    html_out = generate_html_report([doc], workspace_name="Test <Workspace>")

    # Ensure unescaped script tag is not executed
    assert "<script>alert('xss')</script>" not in html_out
    assert "&lt;script&gt;alert(" in html_out or "&lt;script&gt;" in html_out
    assert "Test &lt;Workspace&gt;" in html_out
