"""
Report Builder — select documents and generate a beautiful HTML report.

One click generates a professional, downloadable HTML report
that looks better than most enterprise reporting tools.
"""

from __future__ import annotations
import streamlit as st

from core.workspace import Workspace
from utils.exporter import generate_html_report
import config


def render():
    st.markdown('<div class="page-title">Report Builder</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Select documents and generate a professional intelligence report.</div>',
        unsafe_allow_html=True,
    )

    processed = Workspace.processed()

    if not processed:
        _render_empty_state()
        return

    # ── Document Selection ────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Select Documents</div>', unsafe_allow_html=True)

    col_selectall, col_deselectall, _ = st.columns([2, 2, 4])
    with col_selectall:
        if st.button("✓ Select All", use_container_width=True):
            for doc in processed:
                st.session_state[f"report_select_{doc.id}"] = True
            st.rerun()
    with col_deselectall:
        if st.button("✕ Deselect All", use_container_width=True):
            for doc in processed:
                st.session_state[f"report_select_{doc.id}"] = False
            st.rerun()

    selected_ids: list[str] = []
    for doc in processed:
        key = f"report_select_{doc.id}"
        icon      = config.CATEGORY_ICONS.get(doc.category, "📄")
        cat_color = config.CATEGORY_COLORS.get(doc.category, "#64748b")

        col_check, col_info = st.columns([1, 8])
        with col_check:
            st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
            checked = st.checkbox("", key=key, label_visibility="collapsed")
        with col_info:
            st.markdown(
                f'<div class="clarity-card" style="margin-bottom:8px;padding:14px 18px">'
                f'<div style="display:flex;align-items:center;gap:10px">'
                f'<span style="font-size:22px">{icon}</span>'
                f'<div>'
                f'<div style="font-size:14px;font-weight:600;color:#f1f5f9">{doc.display_name}</div>'
                f'<div style="font-size:12px;color:#64748b">'
                f'<span class="badge" style="background:{cat_color}22;color:{cat_color};border:1px solid {cat_color}55">{doc.category}</span>'
                f'&nbsp;{doc.word_count:,} words · {len(doc.key_facts)} key facts'
                f'</div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        if checked:
            selected_ids.append(doc.id)

    # ── Generate Button ───────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    selected_docs = [Workspace.get(did) for did in selected_ids if Workspace.get(did)]

    if not selected_docs:
        st.info("Select at least one document to generate a report.")
        return

    workspace_name = st.session_state.get("workspace_name", "My Workspace")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            f"📄  Generate Report ({len(selected_docs)} document{'s' if len(selected_docs) != 1 else ''})",
            type="primary",
            use_container_width=True,
        )

    if generate_btn:
        with st.spinner("Generating report…"):
            html_content = generate_html_report(selected_docs, workspace_name)

        st.success("✅ Report generated successfully!")

        # ── Preview ───────────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Report Preview</div>', unsafe_allow_html=True)
        _render_preview(selected_docs, workspace_name)

        # ── Download ──────────────────────────────────────────────────────────
        st.markdown('<div class="section-label">Download</div>', unsafe_allow_html=True)
        col_dl, _ = st.columns([2, 3])
        with col_dl:
            safe_name = workspace_name.lower().replace(" ", "_")
            st.download_button(
                label="⬇️  Download HTML Report",
                data=html_content,
                file_name=f"{safe_name}_clarity_report.html",
                mime="text/html",
                use_container_width=True,
                type="primary",
            )

        st.markdown(
            '<div style="font-size:12px;color:#64748b;margin-top:8px">'
            'The HTML report is fully self-contained and can be opened in any browser, '
            'shared via email, or printed as a PDF.</div>',
            unsafe_allow_html=True,
        )


def _render_preview(selected_docs, workspace_name: str):
    """Show a simplified in-app preview of the report content."""
    from datetime import datetime
    import html

    now = datetime.now().strftime("%B %d, %Y")

    doc_blocks = []
    for doc in selected_docs:
        icon = config.CATEGORY_ICONS.get(doc.category, "📄")
        cat_color = config.CATEGORY_COLORS.get(doc.category, "#64748b")

        facts_html = ""
        for fact in doc.key_facts[:3]:
            facts_html += f'<div style="padding:6px 0;border-bottom:1px solid #f1f5f9;font-size:13px;color:#475569">› {html.escape(fact)}</div>'

        summary_preview = html.escape(doc.summary[:300] + ("…" if len(doc.summary) > 300 else ""))
        doc_blocks.append(
            f'<div style="background:white;border:1px solid #e2e8f0;border-radius:8px;padding:20px;margin-bottom:16px">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">'
            f'<span style="font-size:24px">{icon}</span>'
            f'<div>'
            f'<div style="font-size:16px;font-weight:600;color:#0f172a">{html.escape(doc.display_name)}</div>'
            f'<span style="background:{cat_color}22;color:{cat_color};border:1px solid {cat_color}55;border-radius:12px;padding:2px 10px;font-size:11px;font-weight:600">{html.escape(doc.category)}</span>'
            f'</div>'
            f'</div>'
            f'<p style="font-size:14px;color:#475569;line-height:1.6;margin-bottom:12px">{summary_preview}</p>'
            f'{facts_html}'
            f'</div>'
        )

    all_docs_html = "".join(doc_blocks)
    full_preview_html = (
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:32px;color:#1e293b;font-family:\'Segoe UI\',sans-serif">'
        f'<div style="background:linear-gradient(135deg,#0f172a,#1e3a5f);color:white;padding:28px 32px;border-radius:8px;margin-bottom:24px">'
        f'<div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#6366f1;font-weight:600;margin-bottom:6px">Clarity Workspace · Intelligence Report</div>'
        f'<div style="font-size:24px;font-weight:700;margin-bottom:4px">{html.escape(workspace_name)}</div>'
        f'<div style="font-size:13px;color:#94a3b8">Generated on {now} · {len(selected_docs)} documents</div>'
        f'</div>'
        f'{all_docs_html}'
        f'</div>'
    )

    st.markdown(full_preview_html, unsafe_allow_html=True)


def _render_empty_state():
    st.markdown(
        '<div class="empty-state">'
        '<div class="empty-state-icon">📄</div>'
        '<div class="empty-state-title">No documents available</div>'
        '<div class="empty-state-text">Process documents first to generate a report.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("← Upload Documents", type="primary"):
        Workspace.navigate("upload")
        st.rerun()
