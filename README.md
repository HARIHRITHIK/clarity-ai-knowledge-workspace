# 🔮 Clarity — AI-Powered Knowledge Workspace

> **Turn document chaos into organized intelligence.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat)]()

---

## The Problem

Business teams drown in documents.

A mid-size company accumulates thousands of PDFs, contracts, meeting notes, reports, and spreadsheets. Finding information inside them requires:

- Manually reading every document
- Keyword searching that misses context
- Manually maintaining wikis that go stale
- Waiting for the one person who "knows where that is"

The result: critical information is invisible, decisions are made on incomplete context, and time is wasted on information retrieval instead of analysis.

---

## The Solution

**Clarity** is an AI-powered knowledge workspace that automatically processes your business documents and makes their content instantly accessible.

Upload a document. Clarity classifies it, summarizes it, extracts named entities (people, organizations, dates, amounts), indexes it for semantic search, and makes it available for one-click report generation — all without writing a single query or reading a single page.

```
Upload → AI Analyzes → Knowledge Organized → Search Everything → Generate Reports
```

One sentence: *Upload your business documents and instantly understand what's in them.*

---

## Features

### 📊 Workspace Health Dashboard
A live intelligence panel showing everything your workspace contains at a glance.

| Metric | What It Shows |
|--------|---------------|
| Documents | Total documents in workspace |
| Categories | Auto-detected document types |
| People Mentioned | Unique named individuals across all documents |
| Organizations | Companies and institutions referenced |
| Key Facts | Total AI-extracted facts across the workspace |
| Search Coverage | % of documents indexed for semantic search |

### 🤖 Automatic Document Intelligence
Every uploaded document goes through a 5-stage pipeline:
1. **Parse** — Extract text from PDF, DOCX, TXT, or CSV
2. **Classify** — Detect document type (Financial Report, Meeting Notes, Contract, etc.)
3. **Summarize** — Generate a 3–5 sentence business summary using extractive NLP
4. **Extract** — Identify people, organizations, dates, amounts, and locations (spaCy)
5. **Index** — Build a semantic embedding for search (sentence-transformers)

### 🔍 Semantic Search
Search across your entire document workspace using natural language — not just keywords.

- Finds relevant content even when exact words don't match
- Results ranked by relevance with **High / Medium / Low** confidence labels
- Clickable results open the source document instantly
- Falls back to TF-IDF search if vector model is unavailable (graceful degradation)

### 📋 Report Builder
Select any combination of documents and generate a professional, print-ready HTML report with one click.

- Beautifully styled with professional typography
- Includes: document summaries, key facts, extracted entities, workspace statistics
- Fully self-contained HTML — no external dependencies, shareable by email
- Works as a PDF when printed from the browser

### 🚀 Demo Workspace
A pre-loaded **Acme Corporation** enterprise document set ships with the application:

| Document | Type |
|----------|------|
| Q4 2024 Financial Report | Financial Report |
| Board Meeting Minutes | Meeting Notes |
| Employee Handbook 2025 | HR Policy |
| TechSupply Solutions Contract | Contract / Legal |
| Customer Feedback Report Q4 | Customer Feedback |

A recruiter can click **Open Demo Workspace** and be exploring real content in under 30 seconds — no uploads required.

---

## Architecture

```
clarity/
├── app.py                    ← Entry point, router, home screen
├── config.py                 ← All tunable constants (one place)
│
├── core/
│   ├── document.py           ← Document data model (progressive hydration)
│   ├── workspace.py          ← Session state repository (DB-swappable)
│   └── pipeline.py           ← 5-stage orchestrator
│
├── processors/               ← File format handlers (Abstract Factory pattern)
│   ├── base.py               ← BaseProcessor + factory function
│   ├── pdf_processor.py      ← pypdf
│   ├── docx_processor.py     ← python-docx
│   └── text_processor.py     ← TXT + CSV (pandas)
│
├── intelligence/             ← AI and NLP layer
│   ├── classifier.py         ← TF-IDF keyword classification (offline)
│   ├── summarizer.py         ← Extractive summarization (LSA-inspired)
│   ├── extractor.py          ← spaCy NER + regex fallback
│   └── search.py             ← Semantic search (sentence-transformers + TF-IDF fallback)
│
├── pages/                    ← UI pages (one module per screen)
│   ├── dashboard.py          ← Workspace Health + document library
│   ├── upload.py             ← Upload + demo loader
│   ├── document_view.py      ← Detail: summary, entities, text, export
│   ├── search_page.py        ← Semantic search interface
│   └── report.py             ← Report builder + HTML generation
│
├── utils/
│   └── exporter.py           ← HTML report generator
│
├── assets/
│   └── styles.py             ← Complete CSS design system
│
└── sample_docs/              ← Acme Corporation demo documents
    ├── acme_q4_report.txt
    ├── board_meeting_notes.txt
    ├── employee_handbook.txt
    ├── vendor_contract.txt
    └── customer_feedback.txt
```

### Key Design Decisions

**Why no chatbot?** The value of knowledge management isn't answering questions — it's reducing the need to ask them. Clarity surfaces structure automatically. This is also a deliberate differentiation from the hundreds of "chat with your PDF" portfolio projects that exist.

**Why Streamlit?** Single process, zero infrastructure, free cloud deployment, Python-only codebase. Streamlit is production software used by data teams at Databricks, Snowflake, and hundreds of enterprises. It is not a toy.

**Why no OpenAI API?** Calling an API is not AI engineering. The intelligence in Clarity is built from composable, understood components — a classifier you can explain, a summarizer you can debug, and a search engine whose ranking you can reason about.

**Why graceful degradation?** Every intelligence module has a fallback. The app never crashes because a model isn't installed. This is the correct production approach.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| UI | Streamlit 1.31+ | Application framework |
| Semantic Search | sentence-transformers (all-MiniLM-L6-v2) | Vector embeddings, 80MB, CPU-only |
| Entity Extraction | spaCy (en_core_web_sm) | Named entity recognition |
| Summarization | scikit-learn (TF-IDF) | Extractive sentence scoring |
| Classification | scikit-learn (TF-IDF) | Document type detection |
| PDF Parsing | pypdf | PDF text extraction |
| DOCX Parsing | python-docx | Word document extraction |
| Data | pandas | CSV processing |
| Charts | plotly | Interactive visualizations |

**No paid APIs. No GPU. No internet required after install.**

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/HARIHRITHIK/clarity-ai-knowledge-workspace.git
cd clarity-ai-knowledge-workspace

# 2. Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the spaCy language model
python -m spacy download en_core_web_sm

# 5. Launch the application
streamlit run app.py
```

The application opens at `http://localhost:8501`.

### First Run Notes
- **sentence-transformers** downloads the `all-MiniLM-L6-v2` model (~80MB) on first use. This is a one-time download.
- If the model download fails, the app automatically falls back to TF-IDF search — fully functional, just keyword-based.

---

## Usage

### Try the Demo (30 seconds)
1. Open the application
2. Click **Open Demo Workspace** on the home screen
3. Watch 5 Acme Corporation documents process in real time
4. Explore the Dashboard — see the Workspace Health metrics
5. Click any document to read its AI-generated summary and extracted entities
6. Search "quarterly revenue" or "Sarah Rodriguez" — see semantic results
7. Go to Reports → select all documents → Generate Report → Download

### Upload Your Own Documents
1. Navigate to **Upload** in the sidebar
2. Drag and drop PDF, DOCX, TXT, or CSV files
3. Click **Process Documents**
4. Explore your workspace

---

## Deployment

### Streamlit Community Cloud (Free, Permanent URL)

1. Push the repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select the repository and set `app.py` as the main file
5. Click **Deploy**

Your application is live in 2–3 minutes at a permanent public URL.

### Notes
- Add `python -m spacy download en_core_web_sm` to a `packages.txt` or as a startup command
- The `sentence-transformers` model downloads automatically on first visitor load

---

## Future Roadmap

### v1.1 — Persistence
- [ ] SQLite workspace storage (documents persist across sessions)
- [ ] User-defined workspace names and descriptions
- [ ] Document tags and manual categorization

### v1.2 — Collaboration
- [ ] Multi-user authentication (OAuth / SSO)
- [ ] Shared team workspaces
- [ ] Document commenting and annotations

### v1.3 — Advanced Intelligence
- [ ] PDF table extraction
- [ ] Document similarity clustering
- [ ] Timeline extraction (events sorted chronologically)
- [ ] Scheduled document ingestion (email, Google Drive, SharePoint)

### v2.0 — Enterprise
- [ ] Role-based access control
- [ ] Audit logging
- [ ] API for programmatic document ingestion
- [ ] Webhook notifications on document processing
- [ ] SSO / SAML integration

The architecture is designed for this evolution. Adding persistence requires only replacing `core/workspace.py`. Adding authentication requires only wrapping the router in `app.py`. New document formats require only a new `processors/` file.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## About

Clarity was built as a demonstration of what a software engineer can build when they prioritize **product thinking over feature count**.

The goal was not to demonstrate every AI technique. The goal was to build something that looks like Version 1 of a funded SaaS product — something a recruiter could open, understand in 30 seconds, and immediately think: *"This candidate can build real AI software used inside companies."*

**Built with Python, Streamlit, spaCy, sentence-transformers, and scikit-learn.**

---

*For questions or feedback, open an issue on GitHub.*
