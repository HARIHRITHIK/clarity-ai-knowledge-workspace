"""
Unit tests for the AI & NLP intelligence layer:
- DocumentClassifier (TF-IDF keyword scoring)
- Summarizer (LSA extractive sentence ranking)
- EntityExtractor (spaCy + regex named entity recognition)
- SearchEngine (Semantic search & confidence thresholding)
"""

import pytest
from core.document import Document
from intelligence.classifier import DocumentClassifier
from intelligence.summarizer import Summarizer
from intelligence.extractor import EntityExtractor
from intelligence.search import SearchEngine, embed_text


def test_document_classifier():
    """Test deterministic document classification across standard categories."""
    classifier = DocumentClassifier()

    financial_text = "The quarterly revenue reached $24.7 million with a net profit margin of 14% and strong EBITDA growth."
    cat, conf = classifier.classify(financial_text)
    assert cat == "Financial Report"
    assert conf > 0.0

    hr_text = "All employees are entitled to 20 days of paid time off, medical benefits, and parental leave policy."
    cat, conf = classifier.classify(hr_text)
    assert cat == "HR Policy"
    assert conf > 0.0

    meeting_text = "The board meeting commenced at 9 AM. Attendees discussed the agenda, action items, and next steps."
    cat, conf = classifier.classify(meeting_text)
    assert cat == "Meeting Notes"
    assert conf > 0.0

    empty_cat, empty_conf = classifier.classify("")
    assert empty_cat == "General"
    assert empty_conf == 0.0


def test_extractive_summarizer():
    """Test extractive summary and key facts extraction."""
    summarizer = Summarizer()
    text = (
        "Acme Corporation achieved record annual revenue of $24.7 million in 2024. "
        "The Enterprise SaaS division expanded by 31% year-over-year. "
        "CTO David Kim led the rollout of the new cloud analytics dashboard. "
        "Customer retention reached 112% due to improved onboarding workflows. "
        "Total headcount expanded to 186 employees across three global engineering hubs."
    )

    summary = summarizer.summarize(text, n_sentences=2)
    assert len(summary) > 20
    assert "Acme Corporation" in summary

    facts = summarizer.key_facts(text, n=3)
    assert isinstance(facts, list)
    assert len(facts) >= 2
    assert any("$24.7 million" in f or "186 employees" in f for f in facts)


def test_entity_extractor():
    """Test named entity recognition for people, organizations, dates, amounts."""
    extractor = EntityExtractor()
    text = (
        "On January 15, 2025, CEO Michael Chen and CFO Sarah Rodriguez met with "
        "executives from TechSupply Solutions to finalize a contract worth $180,000 in Austin."
    )

    entities = extractor.extract(text)
    assert isinstance(entities, dict)

    # Check amounts
    amounts = [e.text for e in entities.get("MONEY", [])]
    assert any("$180,000" in a for a in amounts)

    # Check dates
    dates = [e.text for e in entities.get("DATE", [])]
    assert any("January 15, 2025" in d or "2025" in d for d in dates)

    # Check people
    people = [e.text for e in entities.get("PERSON", [])]
    assert any("Michael Chen" in p or "Sarah Rodriguez" in p for p in people)


def test_semantic_search():
    """Test search ranking and High/Medium/Low confidence classification."""
    engine = SearchEngine()

    doc1 = Document(
        id="doc-1",
        filename="q4_financial_report.txt",
        content="Acme Corporation closed Q4 with $7.1 million quarterly revenue and high profit margins.",
        summary="Record quarterly revenue of $7.1 million.",
        key_facts=["Quarterly revenue was $7.1 million."],
        category="Financial Report",
        is_processed=True,
    )
    doc1.embedding = embed_text(doc1.content)

    doc2 = Document(
        id="doc-2",
        filename="employee_handbook.txt",
        content="Acme Corporation offers flexible remote work policies and 20 days paid time off.",
        summary="Employee policy on PTO and remote work.",
        key_facts=["20 days of vacation provided."],
        category="HR Policy",
        is_processed=True,
    )
    doc2.embedding = embed_text(doc2.content)

    # Search for financial term
    results = engine.search("quarterly revenue earnings", [doc1, doc2])
    assert len(results) > 0
    assert results[0].doc_id == "doc-1"
    assert results[0].confidence in ("High", "Medium", "Low")
    assert len(results[0].excerpt) > 10
