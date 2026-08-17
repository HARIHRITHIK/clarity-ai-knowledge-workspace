# 🔮 Clarity — AI-Powered Knowledge Workspace

> **Turn document chaos into organized intelligence.**

[![CI](https://github.com/HARIHRITHIK/clarity-ai-knowledge-workspace/actions/workflows/ci.yml/badge.svg)](https://github.com/HARIHRITHIK/clarity-ai-knowledge-workspace/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

[**⚡ 2-Minute Demo Guide**](DEMO.md) • [**🏛️ System Architecture**](docs/ARCHITECTURE.md) • [**📁 Sample Corpus**](sample_data/)

---

## 📌 The Problem

Business teams accumulate thousands of unstructured PDFs, contracts, meeting notes, reports, and spreadsheets. Retrieving critical context requires:
- Manually reading through lengthy documents
- Brittle keyword search that misses semantic context
- Maintaining internal wikis that go stale
- Relying on tribal knowledge

**Clarity** is a production-grade document intelligence workspace that automatically ingests business files and transforms them into an organized, searchable knowledge base—with zero external API dependencies or cloud costs.

```
Upload Files ➔ AI Analyzes ➔ Knowledge Organized ➔ Semantic Search ➔ Executive Reports
```

---

## 🏛️ System Architecture

```
                 ┌─────────────────┐
                 │  PDF / DOCX /   │
                 │ TXT / CSV       │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Text Extraction │
                 │ (Abstract Fact.)│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Classification  │
                 │ (TF-IDF Scorer) │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              ▼           ▼           ▼
          Summarize      NER      Vector Search
          (LSA-TFIDF)  (spaCy)    (all-MiniLM)
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Core Knowledge  │
                 │ Repository Layer│
                 └────────┬────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
          ┌─────────────┐   ┌─────────────┐
          │ Interactive │   │ Standalone  │
          │ Dashboard   │   │ HTML Report │
          └─────────────┘   └─────────────┘
```

---

## 💡 Engineering Decisions & Trade-Offs

* **Offline-First & Zero API Dependency**:
  Running 100% on local CPU models (spaCy, scikit-learn, sentence-transformers) ensures zero API costs, zero network latency, 100% data privacy, and immunity to third-party rate limits.
* **Extractive Summarization over Generative LLMs**:
  Scores and selects the top factual sentences directly from source text using TF-IDF term matrices. This guarantees **zero generative hallucination** for financial figures, legal clauses, and dates.
* **Abstract Factory File Processors**:
  Text extraction (`PDFProcessor`, `DOCXProcessor`, `TextProcessor`) is fully decoupled from pipeline orchestration, allowing new formats to be added without modifying core business logic.
* **Graceful Degradation**:
  Semantic search leverages `sentence-transformers` vector embeddings with automated fallback to TF-IDF cosine similarity if weights are unavailable. Every component is designed to never crash.

---

## ✨ Features

### 📊 Workspace Health Dashboard
Aggregates enterprise-level intelligence across the document library:
* **Documents & Word Counts**: Total library inventory.
* **Auto-Detected Categories**: Financial Reports, Meeting Notes, Contracts, HR Policies, Customer Feedback, Project Briefs.
* **Named Entities**: Unique people, organizations, dates, and amounts.
* **Interactive Visualizations**: Category distribution donut chart and document size bar chart (Plotly).

### 🤖 5-Stage Document Pipeline
Every uploaded file undergoes an isolated 5-stage transformation:
1. **Parse**: Text extraction with encoding fallbacks (PDF, DOCX, TXT, CSV).
2. **Classify**: Deterministic keyword scoring against curated business domain models.
3. **Summarize**: 4-sentence extractive executive summary + top 6 key facts.
4. **Extract Entities**: spaCy neural NER with regex pattern supplement (`PERSON`, `ORG`, `DATE`, `MONEY`, `GPE`).
5. **Index**: Dense vector embeddings with confidence rating (`High`, `Medium`, `Low`).

### 📄 Executive HTML Report Generator
Generates standalone, print-ready HTML executive reports with complete metadata, summaries, key facts, and entity chips—sanitized against XSS injection and printable as PDF.

---

## 📂 Project Structure

```
clarity/
├── app.py                    ← Streamlit application entry point & router
├── config.py                 ← Centralized tunable constants
│
├── core/
│   ├── document.py           ← Document data model (progressive hydration)
│   ├── workspace.py          ← In-memory repository layer (DB-swappable)
│   └── pipeline.py           ← 5-stage processing orchestrator
│
├── processors/               ← File handlers (Abstract Factory pattern)
│   ├── base.py               ← BaseProcessor & factory registry
│   ├── pdf_processor.py      ← pypdf integration
│   ├── docx_processor.py     ← python-docx integration
│   └── text_processor.py     ← TXT & CSV tabular parser
│
├── intelligence/             ← AI & NLP components
│   ├── classifier.py         ← TF-IDF keyword classification
│   ├── summarizer.py         ← LSA extractive sentence ranking
│   ├── extractor.py          ← spaCy NER + regex fallback
│   └── search.py             ← Vector search + TF-IDF fallback
│
├── pages/                    ← Modular UI screens
│   ├── dashboard.py          ← Workspace Health & library management
│   ├── upload.py             ← Multi-format uploader & demo loader
│   ├── document_view.py      ← Document detail, summary, entities & export
│   ├── search_page.py        ← Semantic search & confidence filters
│   └── report.py             ← HTML report builder & live preview
│
├── sample_data/              ← Multi-format sample files for testing & demos
│   ├── company_report.pdf
│   ├── employee_policy.docx
│   ├── project_notes.txt
│   └── sales_summary.csv
│
├── tests/                    ← Automated pytest suite
│   ├── test_processors.py
│   ├── test_intelligence.py
│   ├── test_pipeline.py
│   └── test_exporter.py
│
├── scripts/
│   ├── benchmark.py          ← Reproducible throughput & latency benchmark
│   └── generate_sample_data.py
│
├── docs/
│   └── ARCHITECTURE.md       ← In-depth architectural documentation
│
└── DEMO.md                   ← Recruiter 2-minute walkthrough guide
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10 or 3.11
- pip

### 1. Clone & Setup
```bash
git clone https://github.com/HARIHRITHIK/clarity-ai-knowledge-workspace.git
cd clarity-ai-knowledge-workspace

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run the Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser. Click **`🚀 Open Demo Workspace`** to load the pre-built Acme Corporation dataset in 2 seconds.

---

## 🧪 Testing & Benchmarks

### Run Automated Tests
```bash
pytest -v
```

### Run Performance Benchmark
```bash
python scripts/benchmark.py
```

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.
