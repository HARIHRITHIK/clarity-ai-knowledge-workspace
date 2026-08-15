"""
Semantic search page — workspace-wide search with confidence labels.

Replaces raw similarity scores with High / Medium / Low confidence badges.
Results are clickable — clicking opens the document detail view.
"""

from __future__ import annotations
import streamlit as st

from core.workspace import Workspace
from intelligence.search import SearchEngine
import config


_engine = SearchEngine()


def render():
    st.markdown('<div class="page-title">Search Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="page-subtitle">Semantic search across {Workspace.count()} document'
        f'{"s" if Workspace.count() != 1 else ""}</div>',
        unsafe_allow_html=True,
    )

    if Workspace.is_empty():
        _render_empty_state()
        return

    # Handle pending query from suggestion clicks before text input is rendered
    if "pending_search_query" in st.session_state:
        q_val = st.session_state.pop("pending_search_query")
        st.session_state["search_input_field"] = q_val
        st.session_state["search_query"] = q_val

    # ── Search input & controls ───────────────────────────────────────────────
    current_query = st.session_state.get("search_query", "")

    if current_query:
        col_input, col_search, col_clear = st.columns([4, 1, 1])
    else:
        col_input, col_search = st.columns([5, 1])
        col_clear = None

    # Initialize search_input_field key in session state if missing
    if "search_input_field" not in st.session_state:
        st.session_state["search_input_field"] = st.session_state.get("search_query", "")

    with col_input:
        query = st.text_input(
            "search_query",
            placeholder="Search anything — people, topics, amounts, decisions…",
            label_visibility="collapsed",
            key="search_input_field",
        )
    with col_search:
        st.button("Search", type="primary", use_container_width=True)

    if col_clear is not None:
        with col_clear:
            if st.button("✕ Clear", type="secondary", use_container_width=True):
                st.session_state["pending_search_query"] = ""
                st.rerun()

    # Persist query across navigation
    st.session_state["search_query"] = query

    # ── Engine info ───────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-size:11px;color:#475569;margin-bottom:16px">'
        f'Engine: {_engine.engine_name}</div>',
        unsafe_allow_html=True,
    )

    # ── Quick search suggestions ───────────────────────────────────────────────
    if not query:
        _render_suggestions()
        return

    # ── Run search ────────────────────────────────────────────────────────────
    docs = Workspace.processed()
    results = _engine.search(query, docs)

    if not results:
        st.markdown(
            f'<div class="empty-state">'
            f'<div class="empty-state-icon">🔍</div>'
            f'<div class="empty-state-title">No results for "{query}"</div>'
            f'<div class="empty-state-text">Try different keywords or broader terms.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        return

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-size:13px;color:#64748b;margin-bottom:16px">'
        f'{len(results)} result{"s" if len(results) > 1 else ""} found for "{query}"</div>',
        unsafe_allow_html=True,
    )

    for result in results:
        _render_result(result)


def _render_result(result):
    """Render a single search result card."""
    doc = Workspace.get(result.doc_id)
    if not doc:
        return

    icon      = config.CATEGORY_ICONS.get(result.category, "📄")
    cat_color = config.CATEGORY_COLORS.get(result.category, "#64748b")

    confidence_class = {
        "High":   "badge-confidence-high",
        "Medium": "badge-confidence-medium",
        "Low":    "badge-confidence-low",
    }.get(result.confidence, "badge-confidence-low")

    col_result, col_btn = st.columns([7, 1])
    with col_result:
        st.markdown(
            f'<div class="search-result">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">'
            f'<span style="font-size:20px">{icon}</span>'
            f'<span class="search-result-title">{doc.display_name}</span>'
            f'<span class="badge" style="background:{cat_color}22;color:{cat_color};border:1px solid {cat_color}55">{result.category}</span>'
            f'<span class="badge {confidence_class}">{result.confidence} Confidence</span>'
            f'</div>'
            f'<div class="search-result-excerpt">{result.excerpt}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_btn:
        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
        if st.button("View →", key=f"search_open_{result.doc_id}", type="secondary"):
            Workspace.navigate("document", result.doc_id)
            st.rerun()


def _render_suggestions():
    """Show clickable search suggestions when no query is entered."""
    suggestions = [
        "quarterly revenue",
        "action items",
        "Sarah Rodriguez",
        "TechSupply Solutions",
        "customer feedback",
        "engineering team",
        "2025 budget",
        "NPS score",
    ]

    st.markdown('<div class="section-label">Try These Searches</div>', unsafe_allow_html=True)

    # Clickable buttons rendered in a clean grid
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions[:8]):
        with cols[i % 4]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                st.session_state["pending_search_query"] = suggestion
                st.rerun()


def _render_empty_state():
    if st.button("← Go to Upload", type="primary"):
        Workspace.navigate("upload")
        st.rerun()
    st.markdown(
        '<div class="empty-state">'
        '<div class="empty-state-icon">🔍</div>'
        '<div class="empty-state-title">No documents in workspace</div>'
        '<div class="empty-state-text">Upload documents or load the demo workspace to start searching.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
