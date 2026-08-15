"""
HTML report exporter.

Generates a standalone, beautifully styled HTML report from selected
workspace documents. The report is self-contained (no external CDN,
no JS required) and renders professionally when printed.
"""

from __future__ import annotations
import html
from datetime import datetime
from typing import List

from core.document import Document
import config


def generate_html_report(documents: List[Document], workspace_name: str) -> str:
    """
    Produce a styled HTML report from the given documents.

    Args:
        documents:      List of processed Document objects to include.
        workspace_name: The workspace/company name shown in the header.

    Returns:
        Complete HTML string ready for download.
    """
    now = datetime.now().strftime("%B %d, %Y")
    doc_count = len(documents)
    safe_workspace_name = html.escape(workspace_name)

    # Collect workspace-wide stats
    all_people:  set[str] = set()
    all_orgs:    set[str] = set()
    all_facts:   int      = 0
    categories:  set[str] = set()

    for doc in documents:
        categories.add(doc.category)
        all_facts += len(doc.key_facts)
        for e in doc.entities.get("PERSON", []):
            all_people.add(e.text.title())
        for e in doc.entities.get("ORG", []):
            all_orgs.add(e.text.title())

    # ── CSS ───────────────────────────────────────────────────────────────────
    css = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #f8fafc;
        color: #1e293b;
        line-height: 1.6;
    }
    .page-wrap { max-width: 900px; margin: 0 auto; padding: 40px 24px 80px; }

    /* Header */
    .report-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        color: white;
        padding: 48px 40px 40px;
        border-radius: 12px;
        margin-bottom: 32px;
    }
    .report-header .brand { font-size: 13px; letter-spacing: 2px; text-transform: uppercase;
                            color: #6366f1; font-weight: 600; margin-bottom: 8px; }
    .report-header h1 { font-size: 32px; font-weight: 700; margin-bottom: 6px; }
    .report-header .meta { font-size: 14px; color: #94a3b8; }

    /* Stats bar */
    .stats-bar {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }
    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-card .value { font-size: 28px; font-weight: 700; color: #6366f1; }
    .stat-card .label { font-size: 12px; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

    /* Section headers */
    .section-title {
        font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
        color: #6366f1; font-weight: 600; margin: 40px 0 16px;
        padding-bottom: 8px; border-bottom: 2px solid #e2e8f0;
    }

    /* Document cards */
    .doc-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 28px;
        margin-bottom: 20px;
    }
    .doc-card-header { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; }
    .doc-icon { font-size: 24px; }
    .doc-meta .doc-name { font-size: 18px; font-weight: 600; color: #0f172a; }
    .doc-meta .doc-info { font-size: 13px; color: #64748b; margin-top: 2px; }
    .category-badge {
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600; letter-spacing: 0.3px;
        background: #ede9fe; color: #6d28d9; margin-left: 8px;
    }

    /* Summary */
    .summary-text { font-size: 15px; color: #334155; margin-bottom: 20px; line-height: 1.7; }

    /* Key facts */
    .facts-title { font-size: 12px; font-weight: 600; color: #64748b;
                   text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
    .fact-item {
        display: flex; gap: 10px; align-items: flex-start;
        padding: 8px 0; border-bottom: 1px solid #f1f5f9;
        font-size: 14px; color: #475569;
    }
    .fact-item:last-child { border-bottom: none; }
    .fact-bullet { color: #6366f1; font-weight: 700; flex-shrink: 0; }

    /* Entities */
    .entity-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
    .entity-chip {
        padding: 4px 12px; border-radius: 20px; font-size: 12px;
        font-weight: 500; border: 1px solid;
    }
    .entity-section-label { font-size: 11px; font-weight: 600; color: #94a3b8;
                            text-transform: uppercase; letter-spacing: 0.5px;
                            margin: 12px 0 6px; }

    /* Footer */
    .report-footer {
        margin-top: 48px; padding-top: 24px; border-top: 1px solid #e2e8f0;
        text-align: center; font-size: 13px; color: #94a3b8;
    }
    .clarity-badge { color: #6366f1; font-weight: 600; }

    @media print {
        .page-wrap { padding: 20px; }
        .doc-card { page-break-inside: avoid; }
    }
    """

    # ── Stats bar ─────────────────────────────────────────────────────────────
    stats_html = f"""
    <div class="stats-bar">
      <div class="stat-card">
        <div class="value">{doc_count}</div>
        <div class="label">Documents</div>
      </div>
      <div class="stat-card">
        <div class="value">{len(categories)}</div>
        <div class="label">Categories</div>
      </div>
      <div class="stat-card">
        <div class="value">{len(all_people)}</div>
        <div class="label">People Mentioned</div>
      </div>
      <div class="stat-card">
        <div class="value">{all_facts}</div>
        <div class="label">Key Facts</div>
      </div>
    </div>
    """

    # ── Document sections ─────────────────────────────────────────────────────
    doc_sections = []
    for doc in documents:
        icon = config.CATEGORY_ICONS.get(doc.category, "📄")
        color = config.CATEGORY_COLORS.get(doc.category, "#64748b")
        safe_name = html.escape(doc.display_name)
        safe_category = html.escape(doc.category)
        safe_summary = html.escape(doc.summary or "No summary available.")

        # Key facts
        facts_html = ""
        if doc.key_facts:
            fact_items = "".join(
                f'<div class="fact-item"><span class="fact-bullet">›</span>{html.escape(fact)}</div>'
                for fact in doc.key_facts[:5]
            )
            facts_html = f"""
            <div class="facts-title">Key Facts</div>
            {fact_items}
            """

        # Entities
        entity_sections = []
        label_display = {
            "PERSON": ("People", "#ede9fe", "#6d28d9"),
            "ORG":    ("Organizations", "#dcfce7", "#15803d"),
            "DATE":   ("Dates", "#fef9c3", "#a16207"),
            "MONEY":  ("Amounts", "#fce7f3", "#be185d"),
            "GPE":    ("Locations", "#cffafe", "#0e7490"),
        }
        for label, (disp_name, bg, fg) in label_display.items():
            ents = doc.entities.get(label, [])
            if ents:
                chips = "".join(
                    f'<span class="entity-chip" style="background:{bg};color:{fg};border-color:{fg}33">'
                    f'{html.escape(e.text)}</span>'
                    for e in ents[:8]
                )
                entity_sections.append(
                    f'<div class="entity-section-label">{disp_name}</div>'
                    f'<div class="entity-grid">{chips}</div>'
                )

        entity_html = "".join(entity_sections)

        word_info = f"{doc.word_count:,} words · {doc.file_type.upper()}"
        doc_sections.append(f"""
        <div class="doc-card">
          <div class="doc-card-header">
            <div class="doc-icon">{icon}</div>
            <div class="doc-meta">
              <div class="doc-name">
                {safe_name}
                <span class="category-badge">{safe_category}</span>
              </div>
              <div class="doc-info">{word_info}</div>
            </div>
          </div>
          <p class="summary-text">{safe_summary}</p>
          {facts_html}
          {entity_html}
        </div>
        """)

    docs_html = "\n".join(doc_sections)

    # ── Full HTML ─────────────────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Clarity Report — {safe_workspace_name}</title>
  <style>{css}</style>
</head>
<body>
  <div class="page-wrap">

    <div class="report-header">
      <div class="brand">Clarity Workspace · Intelligence Report</div>
      <h1>{safe_workspace_name}</h1>
      <div class="meta">Generated on {now} · {doc_count} document{"s" if doc_count != 1 else ""} included</div>
    </div>

    {stats_html}

    <div class="section-title">Document Intelligence</div>
    {docs_html}

    <div class="report-footer">
      Generated by <span class="clarity-badge">Clarity Workspace</span> ·
      AI-Powered Knowledge Management · {now}
    </div>

  </div>
</body>
</html>"""
