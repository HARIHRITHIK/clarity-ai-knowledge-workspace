"""
Clarity Workspace — AI-Powered Knowledge Management Platform
============================================================

Entry point. Handles:
  - Session state initialisation
  - CSS injection
  - Sidebar navigation
  - Page routing
  - Home screen (first launch experience)

Architecture note: This file is intentionally thin.
All logic lives in the page modules under pages/.
"""

from __future__ import annotations
import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Clarity — AI Knowledge Workspace",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports after page config ─────────────────────────────────────────────────
from core.workspace import Workspace
from assets.styles import STYLES

import pages.dashboard      as dashboard_page
import pages.upload         as upload_page
import pages.document_view  as document_view_page
import pages.search_page    as search_page
import pages.report         as report_page

# ── Initialise session state ──────────────────────────────────────────────────
Workspace.init()

# ── Inject design system ──────────────────────────────────────────────────────
st.markdown(STYLES, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        # Logo / Brand
        st.markdown(
            '<div style="padding:20px 8px 24px">'
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">'
            '<div style="width:34px;height:34px;border-radius:8px;'
            'background:linear-gradient(135deg,#6366f1,#8b5cf6);'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:18px">🔮</div>'
            '<div>'
            '<div style="font-size:18px;font-weight:800;color:#f1f5f9;letter-spacing:-0.3px">Clarity</div>'
            '<div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1px">Knowledge Workspace</div>'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Navigation items
        nav_items = [
            ("home",      "🏠", "Home"),
            ("dashboard", "📊", "Dashboard"),
            ("upload",    "⬆️", "Upload"),
            ("search",    "🔍", "Search"),
            ("report",    "📄", "Reports"),
        ]

        current = st.session_state.get("current_page", "home")

        for page_key, icon, label in nav_items:
            is_active = current == page_key
            btn_style = "primary" if is_active else "secondary"
            prefix    = "▸ " if is_active else "  "
            if st.button(
                f"{prefix}{icon}  {label}",
                key=f"nav_{page_key}",
                use_container_width=True,
                type=btn_style if is_active else "secondary",
            ):
                Workspace.navigate(page_key)
                st.rerun()

        # Workspace stats in sidebar
        st.markdown("<hr>", unsafe_allow_html=True)
        stats = Workspace.stats()
        if stats["total_documents"] > 0:
            workspace_name = st.session_state.get("workspace_name", "My Workspace")
            st.markdown(
                f'<div style="padding:12px 8px">'
                f'<div style="font-size:10px;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px">Active Workspace</div>'
                f'<div style="font-size:13px;font-weight:600;color:#f1f5f9;margin-bottom:8px">{workspace_name}</div>'
                f'<div style="font-size:12px;color:#64748b;line-height:1.8">'
                f'📂 {stats["total_documents"]} documents<br>'
                f'🏷️ {stats["categories"]} categories<br>'
                f'👤 {stats["people_mentioned"]} people<br>'
                f'💡 {stats["key_facts"]} key facts'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Clear workspace button
            st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)
            if st.button("🗑️  Clear Workspace", use_container_width=True):
                Workspace.clear()
                Workspace.navigate("home")
                st.rerun()

        # Footer
        st.markdown(
            '<div style="position:fixed;bottom:20px;left:0;width:240px;padding:0 16px;font-size:11px;color:#334155;text-align:center">'
            'Clarity v1.0 · Built with Python<br>'
            '<span style="color:#6366f1">AI Knowledge Management</span>'
            '</div>',
            unsafe_allow_html=True,
        )


# ── Home Screen ───────────────────────────────────────────────────────────────

def render_home():
    """First-launch experience. Never shows an empty state."""

    # Hero
    st.markdown(
        '<div style="text-align:center;padding:40px 24px 32px">'
        '<div style="display:inline-flex;align-items:center;gap:12px;margin-bottom:20px">'
        '<div style="width:56px;height:56px;border-radius:14px;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:28px;box-shadow:0 8px 24px #6366f144">🔮</div>'
        '<div style="font-size:42px;font-weight:800;color:#f1f5f9;letter-spacing:-1px">Clarity</div>'
        '</div>'
        '<div style="font-size:20px;color:#94a3b8;margin-bottom:8px;font-weight:400">Turn document chaos into organized intelligence.</div>'
        '<div style="font-size:14px;color:#475569;max-width:560px;margin:0 auto;line-height:1.6">Upload your business documents. Clarity automatically organizes, summarizes, and extracts insights — giving your team a shared knowledge workspace.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Primary CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🚀  Open Demo Workspace",
            type="primary",
            use_container_width=True,
            key="home_demo_btn",
        ):
            Workspace.navigate("upload")
            st.session_state["trigger_demo"] = True
            st.rerun()

        st.markdown(
            '<div style="text-align:center;margin-top:10px">'
            '<span style="font-size:12px;color:#475569">or </span>'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "⬆️  Upload My Documents",
            use_container_width=True,
            key="home_upload_btn",
        ):
            Workspace.navigate("upload")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # How It Works
    st.markdown(
        '<div style="text-align:center;font-size:11px;font-weight:600;color:#6366f1;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:20px">How It Works</div>',
        unsafe_allow_html=True,
    )

    steps = [
        ("📄", "Upload Documents", "PDF, DOCX, TXT, CSV — any format"),
        ("🤖", "AI Analyzes",      "Classify, summarize, extract entities"),
        ("📊", "Knowledge Organized", "Categories, facts, people, dates"),
        ("🔍", "Search Everything",  "Semantic search across all docs"),
        ("📋", "Generate Reports",   "Beautiful HTML reports in one click"),
    ]

    cols = st.columns(len(steps))
    for i, (icon, title, desc) in enumerate(steps):
        with cols[i]:
            connector = "→" if i < len(steps) - 1 else ""
            st.markdown(
                f'<div style="text-align:center;padding:0 8px">'
                f'<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:22px;margin:0 auto 12px;box-shadow:0 0 0 4px #1e293b,0 0 0 6px #6366f133">{icon}</div>'
                f'<div style="font-size:13px;font-weight:600;color:#f1f5f9;margin-bottom:4px">{title}</div>'
                f'<div style="font-size:11px;color:#64748b;line-height:1.4">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Value propositions
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-size:11px;font-weight:600;color:#6366f1;'
        'text-transform:uppercase;letter-spacing:2px;margin-bottom:20px">Built For</div>',
        unsafe_allow_html=True,
    )

    personas = [
        ("📋", "Business Analysts",   "Extract insights from large document sets"),
        ("👥", "HR Teams",            "Organize policies, contracts, handbooks"),
        ("⚙️", "Operations Teams",    "Centralize vendor agreements and SLAs"),
        ("💬", "Customer Success",    "Analyze feedback patterns at scale"),
        ("💼", "Sales Teams",         "Surface intelligence from deal documents"),
    ]

    p_cols = st.columns(len(personas))
    for i, (icon, title, desc) in enumerate(personas):
        with p_cols[i]:
            st.markdown(
                f'<div class="clarity-card" style="text-align:center;padding:20px 12px">'
                f'<div style="font-size:28px;margin-bottom:8px">{icon}</div>'
                f'<div style="font-size:13px;font-weight:600;color:#f1f5f9;margin-bottom:4px">{title}</div>'
                f'<div style="font-size:11px;color:#64748b;line-height:1.4">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Router ────────────────────────────────────────────────────────────────────

def main():
    render_sidebar()

    page = st.session_state.get("current_page", "home")

    if page == "home":
        render_home()
    elif page == "dashboard":
        dashboard_page.render()
    elif page == "upload":
        upload_page.render()
    elif page == "document":
        document_view_page.render()
    elif page == "search":
        search_page.render()
    elif page == "report":
        report_page.render()
    else:
        render_home()


if __name__ == "__main__":
    main()
