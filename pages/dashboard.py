"""
Dashboard page — Workspace Health + document library.

This is the primary screen. Recruiter lands here after loading the demo.
Every number visible here should tell the story of what the workspace contains.
"""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from core.workspace import Workspace
import config


def render_metric_card(value, label: str, icon: str, color_class: str) -> str:
    display = f"{value:,}" if isinstance(value, int) else str(value)
    return (
        f'<div class="metric-card {color_class}">'
        f'<div class="metric-icon">{icon}</div>'
        f'<div class="metric-value">{display}</div>'
        f'<div class="metric-label">{label}</div>'
        f'</div>'
    )


def render():
    docs = Workspace.all()
    processed = Workspace.processed()
    stats = Workspace.stats()

    # ── Workspace Health Header ───────────────────────────────────────────────
    workspace_name = st.session_state.get("workspace_name", "My Workspace")
    is_demo = any(d.is_demo for d in docs)

    if is_demo:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">'
            f'<div style="font-size:26px;font-weight:800;color:#f1f5f9">{workspace_name}</div>'
            f'<span class="badge" style="background:#1e293b;color:#6366f1;border:1px solid #6366f1;font-size:11px">Demo Workspace</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="page-title">{workspace_name}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="page-subtitle">Workspace Intelligence Dashboard · '
        f'{stats["processed_documents"]} document{"s" if stats["processed_documents"] != 1 else ""} processed</div>',
        unsafe_allow_html=True,
    )

    if Workspace.is_empty():
        _render_empty_state()
        return

    # ── Workspace Health Metrics ──────────────────────────────────────────────
    st.markdown('<div class="section-label">Workspace Health</div>', unsafe_allow_html=True)

    cards = [
        (stats["total_documents"],    "Documents",          "📂", "indigo"),
        (stats["categories"],          "Categories",         "🏷️", "emerald"),
        (stats["people_mentioned"],    "People Mentioned",   "👤", "amber"),
        (stats["organizations"],       "Organizations",      "🏢", "pink"),
        (stats["key_facts"],           "Key Facts",          "💡", "cyan"),
        (f"{stats['search_coverage']}%", "Search Coverage", "🔍", "slate"),
    ]

    cards_html = "".join(render_metric_card(*c) for c in cards)
    st.markdown(
        f'<div class="metric-grid">{cards_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Charts row ────────────────────────────────────────────────────────────
    if len(processed) >= 2:
        col1, col2 = st.columns([1, 1])

        # Category distribution
        with col1:
            category_counts: dict[str, int] = {}
            for doc in processed:
                category_counts[doc.category] = category_counts.get(doc.category, 0) + 1

            colors = [config.CATEGORY_COLORS.get(c, "#64748b") for c in category_counts.keys()]
            fig = go.Figure(data=[go.Pie(
                labels=list(category_counts.keys()),
                values=list(category_counts.values()),
                hole=0.58,
                marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
                textinfo="percent",
                textposition="inside",
                insidetextfont=dict(size=12, color="#ffffff", family="Inter"),
                hovertemplate="<b>%{label}</b><br>%{value} document(s) (%{percent})<extra></extra>",
            )])
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(family="Inter", size=11, color="#cbd5e1"),
                ),
                margin=dict(t=15, b=15, l=15, r=10),
                height=260,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8"),
                annotations=[dict(
                    text=f"<b>{len(processed)}</b><br><span style='font-size:10px;color:#64748b'>DOCS</span>",
                    font=dict(size=14, color="#f1f5f9", family="Inter"),
                    showarrow=False,
                )],
            )
            st.markdown(
                '<div style="font-size:12px;font-weight:600;color:#64748b;'
                'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">'
                'Document Categories</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Word count per document
        with col2:
            sorted_docs = sorted(processed, key=lambda d: d.word_count, reverse=True)[:8]
            names  = [d.display_name[:18] + ("…" if len(d.display_name) > 18 else "") for d in sorted_docs]
            counts = [d.word_count for d in sorted_docs]
            bar_colors = [config.CATEGORY_COLORS.get(d.category, "#64748b") for d in sorted_docs]
            max_c = max(counts) if counts else 1000

            fig2 = go.Figure(go.Bar(
                x=counts, y=names,
                orientation="h",
                marker=dict(color=bar_colors, opacity=0.9),
                text=[f"{c:,} words" for c in counts],
                textposition="outside",
                textfont=dict(size=11, color="#cbd5e1", family="Inter"),
                hovertemplate="<b>%{y}</b><br>%{x:,} words<extra></extra>",
            ))
            fig2.update_layout(
                margin=dict(t=15, b=15, l=10, r=40),
                height=260,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#94a3b8"),
                xaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False,
                    range=[0, max_c * 1.38],  # Headroom so text labels never crop
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=11, color="#cbd5e1", family="Inter"),
                    autorange="reversed",  # Largest on top
                ),
                bargap=0.28,
            )
            st.markdown(
                '<div style="font-size:12px;font-weight:600;color:#64748b;'
                'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">'
                'Document Size (words)</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── Document Library ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Document Library</div>', unsafe_allow_html=True)

    # Sort options
    sort_col, _ = st.columns([2, 5])
    with sort_col:
        sort_by = st.selectbox(
            "Sort by",
            ["Date Added", "Name", "Word Count", "Category"],
            label_visibility="collapsed",
        )

    if sort_by == "Name":
        sorted_docs_all = sorted(docs, key=lambda d: d.filename.lower())
    elif sort_by == "Word Count":
        sorted_docs_all = sorted(docs, key=lambda d: d.word_count, reverse=True)
    elif sort_by == "Category":
        sorted_docs_all = sorted(docs, key=lambda d: d.category)
    else:
        sorted_docs_all = list(reversed(docs))  # Most recently added first

    for doc in sorted_docs_all:
        _render_doc_row(doc)


def _render_doc_row(doc):
    """Render a single document row with click-to-view."""
    icon = config.CATEGORY_ICONS.get(doc.category, "📄")
    cat_color = config.CATEGORY_COLORS.get(doc.category, "#64748b")

    col_main, col_action = st.columns([5, 1.5])
    with col_main:
        status = ""
        if doc.has_error:
            status = "⚠️ Processing error"
        elif not doc.is_processed:
            status = "⏳ Processing…"

        words = f"{doc.word_count:,} words" if doc.word_count else ""
        file_type = doc.file_type.upper() if doc.file_type else ""
        meta_parts = [p for p in [file_type, words, status] if p]
        meta = " · ".join(meta_parts)

        st.markdown(
            f'<div class="doc-card">'
            f'<div class="doc-card-icon">{icon}</div>'
            f'<div class="doc-card-body">'
            f'<div class="doc-card-title">{doc.display_name}</div>'
            f'<div class="doc-card-meta">'
            f'<span class="badge" style="background:{cat_color}22;color:{cat_color};border:1px solid {cat_color}55;margin-right:8px">{doc.category}</span>'
            f'{meta}'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_action:
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        col_v, col_d = st.columns([2.5, 1])
        with col_v:
            if st.button("View →", key=f"view_{doc.id}", type="secondary", use_container_width=True):
                Workspace.navigate("document", doc.id)
                st.rerun()
        with col_d:
            if st.button("🗑️", key=f"del_{doc.id}", help="Remove from workspace", use_container_width=True):
                Workspace.remove(doc.id)
                st.rerun()


def _render_empty_state():
    """Show clear onboarding when workspace is empty."""
    st.markdown(
        '<div class="empty-state">'
        '<div class="empty-state-icon">📂</div>'
        '<div class="empty-state-title">Your workspace is empty</div>'
        '<div class="empty-state-text">'
        'Load the demo workspace to explore Clarity instantly,<br>'
        'or upload your own documents to get started.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀  Open Demo Workspace", type="primary", use_container_width=True):
            Workspace.navigate("upload")
            st.session_state["trigger_demo"] = True
            st.rerun()
