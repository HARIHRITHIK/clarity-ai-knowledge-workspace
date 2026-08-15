"""
Global application configuration.
Centralizes all tuneable constants so new environments require
only this file to be changed.
"""

# ── Application Identity ─────────────────────────────────────────────────────
APP_NAME = "Clarity"
APP_TAGLINE = "Turn document chaos into organized intelligence."
APP_VERSION = "1.0.0"

# ── File Handling ─────────────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = ["pdf", "docx", "txt", "csv"]
MAX_FILE_SIZE_MB = 10
MAX_DOCUMENTS_PER_SESSION = 50
MAX_CONTENT_CHARS = 100_000          # Truncate very large documents for performance

# ── Processing ────────────────────────────────────────────────────────────────
SUMMARY_SENTENCE_COUNT = 4           # Number of sentences in auto-summary
KEY_FACTS_COUNT = 6                  # Number of key facts to extract per document
SEARCH_TOP_K = 10                    # Max results returned by semantic search

# ── Confidence Thresholds ─────────────────────────────────────────────────────
CONFIDENCE_HIGH = 0.65               # Similarity score → "High"
CONFIDENCE_MEDIUM = 0.40             # Similarity score → "Medium" (below = "Low")

# ── Document Categories ───────────────────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "Financial Report": [
        "revenue", "profit", "loss", "quarterly", "earnings", "fiscal",
        "balance sheet", "cash flow", "ebitda", "margin", "budget",
        "forecast", "financial", "q1", "q2", "q3", "q4", "annual report",
        "dividend", "expenditure", "liabilities", "assets"
    ],
    "Meeting Notes": [
        "meeting", "agenda", "minutes", "attendees", "action items",
        "discussion", "follow-up", "next steps", "chairperson", "secretary",
        "motion", "adjourned", "present", "absent", "recap", "standup",
        "retrospective", "sprint review", "all-hands"
    ],
    "Contract / Legal": [
        "agreement", "contract", "terms", "clause", "party", "hereby",
        "whereas", "indemnify", "liability", "jurisdiction", "governing law",
        "termination", "confidential", "nda", "non-disclosure", "amendment",
        "effective date", "warranty", "obligations", "breach", "remedy"
    ],
    "HR Policy": [
        "employee", "policy", "handbook", "benefits", "vacation", "pto",
        "leave", "performance", "review", "compensation", "conduct",
        "harassment", "disciplinary", "onboarding", "offboarding",
        "remote work", "hybrid", "diversity", "inclusion", "payroll"
    ],
    "Customer Feedback": [
        "customer", "feedback", "review", "rating", "satisfaction", "nps",
        "complaint", "support", "ticket", "resolution", "experience",
        "product feedback", "feature request", "bug report", "testimonial",
        "churn", "retention", "survey", "csat", "response time"
    ],
    "Project Brief": [
        "project", "milestone", "deliverable", "scope", "requirements",
        "objective", "timeline", "stakeholder", "roadmap", "sprint",
        "backlog", "priority", "resources", "risk", "dependencies",
        "acceptance criteria", "kpi", "success metric", "proposal"
    ],
}

CATEGORY_COLORS = {
    "Financial Report":  "#10b981",   # emerald
    "Meeting Notes":     "#6366f1",   # indigo
    "Contract / Legal":  "#f59e0b",   # amber
    "HR Policy":         "#ec4899",   # pink
    "Customer Feedback": "#06b6d4",   # cyan
    "Project Brief":     "#8b5cf6",   # violet
    "General":           "#64748b",   # slate
}

CATEGORY_ICONS = {
    "Financial Report":  "📈",
    "Meeting Notes":     "📝",
    "Contract / Legal":  "⚖️",
    "HR Policy":         "👥",
    "Customer Feedback": "💬",
    "Project Brief":     "🗂️",
    "General":           "📄",
}

# ── spaCy Entity Labels → Display Names ──────────────────────────────────────
ENTITY_DISPLAY = {
    "PERSON":  ("People",        "#6366f1"),
    "ORG":     ("Organizations", "#10b981"),
    "DATE":    ("Dates",         "#f59e0b"),
    "MONEY":   ("Amounts",       "#ec4899"),
    "GPE":     ("Locations",     "#06b6d4"),
}

# ── Demo Workspace ────────────────────────────────────────────────────────────
DEMO_WORKSPACE_NAME = "Acme Corporation"
DEMO_DOCUMENT_PATHS = [
    "sample_docs/acme_q4_report.txt",
    "sample_docs/board_meeting_notes.txt",
    "sample_docs/employee_handbook.txt",
    "sample_docs/vendor_contract.txt",
    "sample_docs/customer_feedback.txt",
]
