"""
Global CSS design system injected into every Streamlit page.
All visual tokens are defined here — no ad-hoc colors or sizes in page files.
"""

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Root ──────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide Streamlit default auto-generated pages navigation */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavSeparator"],
[data-testid="stSidebarNavItems"],
div[data-testid="stSidebarNav"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Hide Streamlit header buttons, share, deploy, GitHub icons, edit, and footer */
#MainMenu, footer {
    visibility: hidden !important;
    display: none !important;
}
.stDeployButton,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stMainMenu"],
[data-testid="manage-app-button"],
[data-testid="stToolbarActionButton"],
.viewerBadge_container__r5tak,
.viewerBadge_link__1SuGQ {
    display: none !important;
    visibility: hidden !important;
}
.block-container { padding-top: 1.5rem !important; max-width: 1200px; }

/* Keep header transparent without blocking clicks */
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar collapse/expand toggle button (visible when collapsed) */
[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    display: flex !important;
    z-index: 999999 !important;
}

/* Floating expand button when sidebar is collapsed */
[data-testid="collapsedControl"] {
    top: 12px !important;
    left: 12px !important;
    background: #1e293b !important;
    border: 1px solid #6366f1 !important;
    border-radius: 8px !important;
    padding: 4px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="collapsedControl"] svg {
    fill: #818cf8 !important;
    color: #818cf8 !important;
}
[data-testid="collapsedControl"]:hover {
    background: #6366f1 !important;
    border-color: #818cf8 !important;
}
[data-testid="collapsedControl"]:hover svg {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* ── Sidebar ───────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    color: #94a3b8;
    font-size: 14px;
    font-weight: 500;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
    margin-bottom: 2px;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1e293b;
    color: #f1f5f9;
}

/* ── Card Component ────────────────────────────────────────────────── */
.clarity-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 14px;
    transition: border-color 0.2s ease;
}
.clarity-card:hover { border-color: #6366f1; }

/* ── Metric Cards (Workspace Health) ──────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.metric-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 22px 20px;
    text-align: left;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.metric-card.indigo::before  { background: #6366f1; }
.metric-card.emerald::before { background: #10b981; }
.metric-card.amber::before   { background: #f59e0b; }
.metric-card.pink::before    { background: #ec4899; }
.metric-card.cyan::before    { background: #06b6d4; }
.metric-card.slate::before   { background: #64748b; }
.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.metric-icon {
    position: absolute;
    top: 18px; right: 18px;
    font-size: 22px;
    opacity: 0.5;
}

/* ── Document Cards ────────────────────────────────────────────────── */
.doc-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.doc-card:hover {
    border-color: #6366f1;
    background: #1e2d47;
}
.doc-card-icon {
    font-size: 26px;
    flex-shrink: 0;
    margin-top: 2px;
}
.doc-card-body { flex: 1; min-width: 0; }
.doc-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.doc-card-meta {
    font-size: 12px;
    color: #64748b;
}

/* ── Badges ────────────────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2px;
    line-height: 1.8;
}
.badge-confidence-high   { background: #052e16; color: #34d399; border: 1px solid #065f46; }
.badge-confidence-medium { background: #451a03; color: #fbbf24; border: 1px solid #78350f; }
.badge-confidence-low    { background: #1e1b4b; color: #818cf8; border: 1px solid #3730a3; }

/* ── Entity Chips ──────────────────────────────────────────────────── */
.entity-chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
    border: 1px solid;
}
.entity-person { background: #1e1b4b; color: #a5b4fc; border-color: #3730a3; }
.entity-org    { background: #052e16; color: #6ee7b7; border-color: #065f46; }
.entity-date   { background: #451a03; color: #fcd34d; border-color: #78350f; }
.entity-money  { background: #4a044e; color: #f0abfc; border-color: #7e22ce; }
.entity-gpe    { background: #083344; color: #67e8f9; border-color: #0e7490; }

/* ── Section Headers ───────────────────────────────────────────────── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 28px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e293b;
}

/* ── Progress Steps ────────────────────────────────────────────────── */
.progress-steps {
    display: flex;
    align-items: center;
    gap: 4px;
    margin: 12px 0;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #64748b;
}
.step-item.done { color: #10b981; }
.step-item.active { color: #6366f1; }
.step-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #334155;
}
.step-dot.done   { background: #10b981; }
.step-dot.active { background: #6366f1; }
.step-line {
    flex: 1; height: 1px;
    background: #334155;
    min-width: 20px;
}

/* ── How It Works Flow ─────────────────────────────────────────────── */
.how-it-works {
    display: flex;
    align-items: flex-start;
    gap: 0;
    padding: 32px 0 20px;
    overflow-x: auto;
}
.how-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    flex: 1;
    min-width: 120px;
}
.how-step-num {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
    box-shadow: 0 0 0 4px #1e293b, 0 0 0 6px #6366f155;
}
.how-step-icon { font-size: 28px; margin-bottom: 8px; }
.how-step-title {
    font-size: 13px; font-weight: 600;
    color: #f1f5f9; margin-bottom: 4px;
}
.how-step-desc { font-size: 12px; color: #64748b; line-height: 1.4; }
.how-arrow {
    font-size: 20px; color: #334155;
    margin-top: 12px; flex-shrink: 0;
    align-self: flex-start;
    padding-top: 10px;
}

/* ── Search Results ────────────────────────────────────────────────── */
.search-result {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: border-color 0.15s;
}
.search-result:hover { border-color: #6366f1; }
.search-result-title { font-size: 15px; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
.search-result-excerpt { font-size: 13px; color: #94a3b8; line-height: 1.5; margin: 8px 0; }
.search-result-meta { font-size: 12px; color: #64748b; }

/* ── Buttons ───────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    box-shadow: 0 2px 8px #6366f144 !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px #6366f166 !important;
}

/* ── Tabs ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #334155 !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    color: #6366f1 !important;
    border-bottom-color: #6366f1 !important;
}

/* ── Text Inputs ───────────────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px #6366f133 !important;
}

/* ── Dividers ──────────────────────────────────────────────────────── */
hr { border-color: #1e293b !important; }

/* ── Page title ────────────────────────────────────────────────────── */
.page-title {
    font-size: 26px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 28px;
}

/* ── Empty state ───────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 64px 32px;
    color: #64748b;
}
.empty-state-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state-title { font-size: 18px; font-weight: 600; color: #94a3b8; margin-bottom: 8px; }
.empty-state-text  { font-size: 14px; }
</style>
"""
