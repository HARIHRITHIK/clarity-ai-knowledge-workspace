# System Architecture & Technical Design

This document details the software architecture, data flow, component design, and engineering decisions behind **Clarity — AI Knowledge Workspace**.

---

## 1. High-Level Data Flow

```
                      ┌───────────────────────────────┐
                      │   Multi-Format Document Input │
                      │      PDF / DOCX / TXT / CSV   │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │ Stage 1: Text Extraction      │
                      │ (Abstract Factory Processors) │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │ Stage 2: Domain Classifier    │
                      │ (TF-IDF Keyword Frequency)    │
                      └───────────────┬───────────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      ▼                               ▼
       ┌─────────────────────────────┐ ┌─────────────────────────────┐
       │ Stage 3: Extractive Summary │ │ Stage 4: Entity Recognition │
       │ (TF-IDF Sentence Scoring)   │ │ (spaCy NER + Regex Fallback)│
       └──────────────┬──────────────┘ └──────────────┬──────────────┘
                      │                               │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │ Stage 5: Semantic Indexing    │
                      │ (Vector Embedding + TF-IDF)   │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │ Core Workspace Repository     │
                      │ (Progressively Hydrated Model)│
                      └───────────────┬───────────────┘
                                      │
                      ┌───────────────┴───────────────┐
                      ▼                               ▼
       ┌─────────────────────────────┐ ┌─────────────────────────────┐
       │ Interactive Dashboard &     │ │ Standalone HTML Report      │
       │ Semantic Search Engine      │ │ Generator (XSS-Sanitized)   │
       └─────────────────────────────┘ └─────────────────────────────┘
```

---

## 2. Component Structure

### Core Layer (`core/`)
* **`document.py`**: Defines the `Document` and `Entity` data models. Uses progressive hydration—each processing stage populates specific dataclass attributes (`summary`, `key_facts`, `entities`, `category`, `embedding`).
* **`workspace.py`**: In-memory repository layer managing document collections, search indexing, category filtering, and aggregated workspace health statistics.
* **`pipeline.py`**: Orchestrator executing the 5 processing stages sequentially with isolated error boundaries and progress callback hooks.

### Ingestion & Processor Layer (`processors/`)
* Implements the **Abstract Factory** pattern via `BaseProcessor` and `get_processor(extension)`:
  * **`pdf_processor.py`**: Extracts text from PDF pages using `pypdf`.
  * **`docx_processor.py`**: Extracts text from paragraphs and table cells using `python-docx`.
  * **`text_processor.py`**: Handles `.txt` files with multi-encoding fallback (`utf-8`, `latin-1`, `cp1252`) and `.csv` tabular files via `pandas`.

### Intelligence & NLP Layer (`intelligence/`)
* **`classifier.py`**: Deterministic domain classifier computing TF-IDF keyword frequency scores against business categories (*Financial Report*, *HR Policy*, *Meeting Notes*, *Contract / Legal*, *Customer Feedback*, *Project Brief*).
* **`summarizer.py`**: Extractive text summarizer using TF-IDF term matrix sentence scoring. Computes term saliency sums per sentence and returns the top $N$ sentences in original reading order.
* **`extractor.py`**: Named entity recognition for `PERSON`, `ORG`, `DATE`, `MONEY`, and `GPE`. Integrates spaCy's `en_core_web_sm` model with regex pattern fallbacks for currency, dates, and capitalized entities.
* **`search.py`**: Semantic search engine computing cosine similarity over dense `sentence-transformers` embeddings (`all-MiniLM-L6-v2`), with automated fallback to TF-IDF sparse vector cosine similarity for CPU environments.

### UI & Reporting Layer (`pages/` & `utils/`)
* **`pages/`**: Modular Streamlit views (`dashboard.py`, `upload.py`, `document_view.py`, `search_page.py`, `report.py`).
* **`utils/exporter.py`**: Standalone HTML report generator with embedded CSS styling, responsive tables, and strict HTML entity escaping (`html.escape`) to prevent cross-site scripting (XSS).

---

## 3. Engineering Decisions & Design Trade-Offs

| Decision | Implementation | Trade-Off & Rationale |
|---|---|---|
| **Offline-First Execution** | Local CPU inference via spaCy, scikit-learn, and sentence-transformers | Eliminates third-party API costs, network latency, and vendor rate limits while preserving data privacy. |
| **Extractive Summarization** | TF-IDF sentence saliency scoring | Selects verified sentences directly from source text, minimizing the hallucination risks inherent in generative language models. |
| **Abstract Factory Processors** | `BaseProcessor` inheritance | Decouples format-specific text extraction from pipeline orchestration, allowing new file types to be added cleanly. |
| **Multi-Tier Fallback** | Dense vector search ➔ TF-IDF cosine similarity; spaCy NER ➔ Regex patterns | Guarantees system resilience on low-resource environments without unhandled crashes. |
| **Stateless Workspace Interface** | `Workspace` repository pattern | Decouples business logic from Streamlit's session state, simplifying migration to a database backend (e.g. SQLite / PostgreSQL) in future releases. |
