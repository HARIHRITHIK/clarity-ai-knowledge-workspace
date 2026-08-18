"""
Upload page — file upload + demo workspace loader.

This page handles both:
  1. User file uploads (PDF, DOCX, TXT, CSV)
  2. Demo workspace loading (Acme Corporation documents)

Every upload shows a per-file, per-stage progress breakdown
so the recruiter can see the pipeline executing in real time.
"""

from __future__ import annotations
import time
import streamlit as st
from pathlib import Path

from core.workspace import Workspace
from core.pipeline import Pipeline
import config


def render():
    st.markdown('<div class="page-title">Upload Documents</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Add documents to your workspace — '
        'PDF, DOCX, TXT, and CSV supported.</div>',
        unsafe_allow_html=True,
    )

    # ── Auto-trigger demo if navigated from home CTA ──────────────────────────
    if st.session_state.pop("trigger_demo", False):
        _load_demo_workspace()
        return

    tab1, tab2 = st.tabs(["  📁  Upload Files  ", "  🚀  Load Demo Workspace  "])

    with tab1:
        _render_upload_tab()

    with tab2:
        _render_demo_tab()


def _render_upload_tab():
    uploaded_files = st.file_uploader(
        "Drop files here or click to browse",
        type=config.SUPPORTED_EXTENSIONS,
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="file_uploader",
    )

    if uploaded_files:
        if Workspace.count() + len(uploaded_files) > config.MAX_DOCUMENTS_PER_SESSION:
            remaining = config.MAX_DOCUMENTS_PER_SESSION - Workspace.count()
            st.warning(
                f"Workspace limit is {config.MAX_DOCUMENTS_PER_SESSION} documents. "
                f"You can add {remaining} more."
            )
            uploaded_files = uploaded_files[:remaining]

        col1, col2 = st.columns([2, 1])
        with col1:
            process_btn = st.button(
                f"⚡  Process {len(uploaded_files)} document{'s' if len(uploaded_files) > 1 else ''}",
                type="primary",
                use_container_width=True,
            )
        with col2:
            st.caption(f"{len(uploaded_files)} file{'s' if len(uploaded_files) > 1 else ''} selected")

        if process_btn:
            _process_uploads(uploaded_files)


def _render_demo_tab():
    st.markdown(
        '<div class="clarity-card">'
        '<div style="display:flex;align-items:center;gap:14px;margin-bottom:12px">'
        '<div style="font-size:32px">🏢</div>'
        '<div>'
        '<div style="font-size:18px;font-weight:700;color:#f1f5f9">Acme Corporation</div>'
        '<div style="font-size:13px;color:#64748b">Sample enterprise workspace · 5 documents</div>'
        '</div>'
        '</div>'
        '<div style="color:#94a3b8;font-size:14px;line-height:1.6;margin-bottom:16px">'
        'A realistic enterprise document set including a Q4 Financial Report, Board Meeting Notes, '
        'Employee Handbook, Vendor Contract, and Customer Feedback Report. '
        'Loads in seconds. No signup required.'
        '</div>'
        '<div style="display:flex;gap:8px;flex-wrap:wrap">'
        '<span class="badge" style="background:#1e1b4b;color:#a5b4fc;border:1px solid #3730a3">📈 Financial Report</span>'
        '<span class="badge" style="background:#1e293b;color:#818cf8;border:1px solid #6366f1">📝 Meeting Notes</span>'
        '<span class="badge" style="background:#052e16;color:#6ee7b7;border:1px solid #065f46">⚖️ Vendor Contract</span>'
        '<span class="badge" style="background:#4a044e;color:#f0abfc;border:1px solid #7e22ce">👥 HR Policy</span>'
        '<span class="badge" style="background:#083344;color:#67e8f9;border:1px solid #0e7490">💬 Customer Feedback</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    already_loaded = st.session_state.get("demo_loaded", False)

    if already_loaded:
        st.success("✅ Demo workspace is already loaded. Navigate to Dashboard to explore.")
        if st.button("Go to Dashboard →", type="primary"):
            Workspace.navigate("dashboard")
            st.rerun()
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀  Open Demo Workspace", type="primary", use_container_width=True):
                _load_demo_workspace()


def _process_uploads(uploaded_files):
    """Process a list of Streamlit UploadedFile objects."""
    pipeline = Pipeline()
    total = len(uploaded_files)
    success_count = 0

    st.markdown('<div class="section-label">Processing</div>', unsafe_allow_html=True)

    for i, uploaded_file in enumerate(uploaded_files):
        filename = uploaded_file.name
        raw_bytes = uploaded_file.read()

        if len(raw_bytes) > config.MAX_FILE_SIZE_MB * 1024 * 1024:
            st.warning(f"⚠️ {filename} exceeds {config.MAX_FILE_SIZE_MB}MB limit — skipped.")
            continue

        with st.container():
            st.markdown(
                f'<div style="font-size:14px;font-weight:600;color:#f1f5f9;margin-bottom:6px">'
                f'📄 {filename}</div>',
                unsafe_allow_html=True,
            )
            progress_bar = st.progress(0)
            status_text  = st.empty()

            def on_progress(stage: str, pct: int):
                progress_bar.progress(pct / 100)
                status_text.markdown(
                    f'<div style="font-size:12px;color:#64748b">{stage}…</div>',
                    unsafe_allow_html=True,
                )

            doc = pipeline.run(filename, raw_bytes, on_progress=on_progress)

            if doc.has_error:
                status_text.markdown(
                    f'<div style="font-size:12px;color:#ef4444">⚠️ {doc.processing_error}</div>',
                    unsafe_allow_html=True,
                )
            else:
                Workspace.add(doc)
                progress_bar.progress(1.0)
                status_text.markdown(
                    f'<div style="font-size:12px;color:#10b981">'
                    f'✓ Processed · {doc.word_count:,} words · {doc.category}</div>',
                    unsafe_allow_html=True,
                )
                success_count += 1

        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    if success_count > 0:
        st.success(
            f"✅ {success_count} document{'s' if success_count > 1 else ''} added to workspace."
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Dashboard →", type="primary", use_container_width=True):
                Workspace.navigate("dashboard")
                st.rerun()
        with col2:
            if st.button("Upload More", use_container_width=True):
                st.rerun()


def _load_demo_workspace():
    """Load the Acme Corporation demo documents."""
    Workspace.clear()
    pipeline = Pipeline()

    st.markdown('<div class="section-label">Loading Demo Workspace</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:14px;color:#64748b;margin-bottom:16px">'
        'Processing Acme Corporation multi-format documents (PDF, DOCX, TXT, CSV)…</div>',
        unsafe_allow_html=True,
    )

    display_names = {
        "company_report.pdf":    ("📈", "Acme Q4 Financial Report (PDF)"),
        "employee_policy.docx":  ("👥", "Employee Policy Handbook (DOCX)"),
        "project_notes.txt":     ("📝", "Sprint & Architecture Notes (TXT)"),
        "sales_summary.csv":     ("📊", "Enterprise Sales Summary (CSV)"),
    }

    success_count = 0
    for path in config.DEMO_DOCUMENT_PATHS:
        p = Path(path)
        if not p.exists():
            st.warning(f"Demo file not found: {p.name}")
            continue

        fname = p.name
        icon, label = display_names.get(fname, ("📄", fname))

        with st.container():
            st.markdown(
                f'<div style="font-size:14px;font-weight:600;color:#f1f5f9;margin-bottom:6px">'
                f'{icon} {label}</div>',
                unsafe_allow_html=True,
            )
            progress_bar = st.progress(0)
            status_text  = st.empty()

            def on_progress(stage: str, pct: int):
                progress_bar.progress(pct / 100)
                status_text.markdown(
                    f'<div style="font-size:12px;color:#64748b">{stage}…</div>',
                    unsafe_allow_html=True,
                )

            doc = pipeline.run_from_path(str(p), is_demo=True)

            if doc.has_error:
                status_text.markdown(
                    f'<div style="font-size:12px;color:#ef4444">⚠️ {doc.processing_error}</div>',
                    unsafe_allow_html=True,
                )
            else:
                doc.filename = fname
                Workspace.add(doc)
                progress_bar.progress(1.0)
                status_text.markdown(
                    f'<div style="font-size:12px;color:#10b981">'
                    f'✓ {doc.word_count:,} words · {doc.category}</div>',
                    unsafe_allow_html=True,
                )
                success_count += 1

        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

    if success_count > 0:
        st.session_state["demo_loaded"]  = True
        st.session_state["workspace_name"] = config.DEMO_WORKSPACE_NAME
        st.success(
            f"✅ Demo workspace loaded — {success_count} multi-format Acme Corporation documents ready."
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Explore Workspace →", type="primary", use_container_width=True):
                Workspace.navigate("dashboard")
                st.rerun()
