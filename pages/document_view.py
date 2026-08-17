"""
Document detail view — summary, key facts, entities, full text.

This is where recruiter spends the most time per document.
Every section should communicate AI value clearly.
"""

from __future__ import annotations
import streamlit as st
import json

from core.workspace import Workspace
import config


def render():
    doc_id = st.session_state.get("current_doc_id")
    if not doc_id:
        st.info("Select a document from the dashboard to view it here.")
        return

    doc = Workspace.get(doc_id)
    if not doc:
        st.error("Document not found in workspace.")
        return

    # ── Header ────────────────────────────────────────────────────────────────
    icon      = config.CATEGORY_ICONS.get(doc.category, "📄")
    cat_color = config.CATEGORY_COLORS.get(doc.category, "#64748b")

    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back", type="secondary"):
            Workspace.navigate("dashboard")
            st.rerun()

    with col_title:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">'
            f'<div style="font-size:32px">{icon}</div>'
            f'<div>'
            f'<div class="page-title" style="margin-bottom:2px">{doc.display_name}</div>'
            f'<span class="badge" style="background:{cat_color}22;color:{cat_color};border:1px solid {cat_color}55;font-size:12px">{doc.category}</span>'
            f'<span style="font-size:12px;color:#64748b;margin-left:10px">{doc.word_count:,} words · {doc.file_type.upper()}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    if doc.has_error:
        st.error(f"Processing error: {doc.processing_error}")
        return

    # ── Main tabs ─────────────────────────────────────────────────────────────
    tab_summary, tab_entities, tab_fulltext, tab_export = st.tabs(
        ["  📋  Summary  ", "  🏷️  Entities  ", "  📄  Full Text  ", "  ⬇️  Export  "]
    )

    with tab_summary:
        _render_summary_tab(doc)

    with tab_entities:
        _render_entities_tab(doc)

    with tab_fulltext:
        _render_fulltext_tab(doc)

    with tab_export:
        _render_export_tab(doc)


def _render_summary_tab(doc):
    # AI Summary
    st.markdown('<div class="section-label">AI Summary</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="clarity-card" style="font-size:15px;color:#cbd5e1;line-height:1.7">'
        f'{doc.summary or "No summary generated."}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Key Facts
    if doc.key_facts:
        st.markdown('<div class="section-label">Key Facts</div>', unsafe_allow_html=True)
        for i, fact in enumerate(doc.key_facts, 1):
            st.markdown(
                f'<div style="display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #1e293b">'
                f'<div style="width:24px;height:24px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;flex-shrink:0">{i}</div>'
                f'<div style="font-size:14px;color:#cbd5e1;line-height:1.5">{fact}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Quick stats
    st.markdown('<div class="section-label">Document Stats</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Words", f"{doc.word_count:,}")
    with c2:
        st.metric("Key Facts", len(doc.key_facts))
    with c3:
        entity_count = sum(len(v) for v in doc.entities.values())
        st.metric("Entities Found", entity_count)
    with c4:
        indexed = "✓ Indexed" if doc.is_processed else "⏳ Pending"
        st.metric("Search Indexed", indexed)


def _render_entities_tab(doc):
    if not doc.entities:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">🔍</div>'
            '<div class="empty-state-title">No entities extracted</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    label_config = {
        "PERSON": ("People",         "entity-person", "👤"),
        "ORG":    ("Organizations",  "entity-org",    "🏢"),
        "DATE":   ("Dates",          "entity-date",   "📅"),
        "MONEY":  ("Amounts",        "entity-money",  "💰"),
        "GPE":    ("Locations",      "entity-gpe",    "📍"),
    }

    for label, (display_name, chip_class, icon) in label_config.items():
        entities = doc.entities.get(label, [])
        if not entities:
            continue

        st.markdown(
            f'<div class="section-label">{icon} {display_name}</div>',
            unsafe_allow_html=True,
        )

        chips_html = "".join(
            f'<span class="entity-chip {chip_class}">'
            f'{e.text}'
            f'{"&nbsp;·&nbsp;" + str(e.count) if e.count > 1 else ""}'
            f'</span>'
            for e in entities
        )
        st.markdown(
            f'<div style="margin-bottom:8px">{chips_html}</div>',
            unsafe_allow_html=True,
        )

    # Entity summary table
    st.markdown('<div class="section-label">All Entities</div>', unsafe_allow_html=True)
    import pandas as pd
    rows = []
    for label, entities in doc.entities.items():
        display_name = label_config.get(label, (label, "", ""))[0]
        for e in entities:
            rows.append({"Type": display_name, "Entity": e.text, "Mentions": e.count})
    if rows:
        df = pd.DataFrame(rows).sort_values("Mentions", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)


def _render_fulltext_tab(doc):
    st.markdown('<div class="section-label">Document Text</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:13px;color:#64748b;margin-bottom:12px">'
        f'{doc.char_count:,} characters · {doc.word_count:,} words</div>',
        unsafe_allow_html=True,
    )
    st.text_area(
        "full_text",
        value=doc.content,
        height=500,
        disabled=True,
        label_visibility="collapsed",
    )


def _render_export_tab(doc):
    st.markdown('<div class="section-label">Export Options</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="clarity-card" style="text-align:center">'
            '<div style="font-size:32px;margin-bottom:8px">📊</div>'
            '<div style="font-size:15px;font-weight:600;color:#f1f5f9;margin-bottom:4px">'
            'Structured JSON</div>'
            '<div style="font-size:13px;color:#64748b;margin-bottom:16px">'
            'All extracted data as machine-readable JSON</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        export_data = json.dumps(doc.to_dict(), indent=2)
        st.download_button(
            label="⬇️  Download JSON",
            data=export_data,
            file_name=f"{doc.display_name}_clarity.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        import pandas as pd
        import io
        st.markdown(
            '<div class="clarity-card" style="text-align:center">'
            '<div style="font-size:32px;margin-bottom:8px">📋</div>'
            '<div style="font-size:15px;font-weight:600;color:#f1f5f9;margin-bottom:4px">'
            'Entity CSV</div>'
            '<div style="font-size:13px;color:#64748b;margin-bottom:16px">'
            'All extracted entities in spreadsheet format</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        rows = []
        label_names = {
            "PERSON": "Person", "ORG": "Organization",
            "DATE": "Date", "MONEY": "Amount", "GPE": "Location",
        }
        for label, entities in doc.entities.items():
            for e in entities:
                rows.append({
                    "Document": doc.filename,
                    "Type": label_names.get(label, label),
                    "Entity": e.text,
                    "Mentions": e.count,
                })
        if rows:
            df = pd.DataFrame(rows)
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                label="⬇️  Download CSV",
                data=csv_buf.getvalue(),
                file_name=f"{doc.display_name}_entities.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("No entities to export.")
