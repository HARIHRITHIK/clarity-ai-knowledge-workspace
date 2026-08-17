# System Architecture & Technical Design

This document details the software architecture, data flow, component design, and engineering trade-offs behind **Clarity**.

---

## 1. High-Level Data Flow

```
                 ┌────────────────────────────────┐
                 │  Multi-Format Document Input   │
                 │   PDF / DOCX / TXT / CSV       │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ Stage 1: Text Extraction       │
                 │ (Abstract Factory Processors)  │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ Stage 2: Category Classifier   │
                 │ (TF-IDF Keyword Frequency)     │
                 └───────────────┬────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
  ┌─────────────────────────────┐ ┌─────────────────────────────┐
  │ Stage 3: Extractive Summary │ │ Stage 4: Entity Recognition │
  │ (LSA Sentence Importance)   │ │ (spaCy NER + Regex)         │
  └──────────────┬──────────────┘ └──────────────┬──────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ Stage 5: Semantic Indexing     │
                 │ (Vector Embedding + TF-IDF)    │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ Core Workspace Repository      │
                 │ (Progressively Hydrated Model) │
                 └───────────────┬────────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
  ┌─────────────────────────────┐ ┌─────────────────────────────┐
  │ Interactive Dashboard &     │ │ Standalone HTML Report      │
  │ Confidence-Ranked Search    │ │ Generator (Print-Ready)     │
  └─────────────────────────────┘ └─────────────────────────────┘
```

---

## 2. Component Breakdown

### Core (`core/`)
* **`document.py`**: Defines the `Document` and `Entity` dataclasses. Implements progressive hydration—fields are populated sequentially across pipeline stages.
* **`workspace.py`**: In-memory repository layer managing documents, query aggregations, and workspace health statistics. Decoupled from Streamlit session state so it can be swapped to SQLite/PostgreSQL in future iterations.
* **`pipeline.py`**: Orchestrator executing the 5-stage processing pipeline with stage isolation, progress callbacks, and graceful error boundaries.

### Processors (`processors/`)
* Implements the **Abstract Factory** pattern via `BaseProcessor` and `get_processor(extension)`.
* **`pdf_processor.py`**: Uses `pypdf` to extract text from multi-page PDFs.
* **`docx_processor.py`**: Uses `python-docx` to extract text across paragraphs and tables.
* **`text_processor.py`**: Handles `.txt` with encoding fallbacks (UTF-8, Latin-1, CP1252) and `.csv` tabular data formatting via `pandas`.

### Intelligence Layer (`intelligence/`)
* **`classifier.py`**: Deterministic keyword-weighted TF-IDF classifier that maps document text to business categories.
* **`summarizer.py`**: Extractive text summarization using TF-IDF sentence matrix scoring. Ranks and returns top-N sentences in original reading order to avoid hallucinations.
* **`extractor.py`**: Named entity recognition targeting `PERSON`, `ORG`, `DATE`, `MONEY`, and `GPE`. Combines neural spaCy models with high-precision regex fallback patterns.
* **`search.py`**: Vector semantic search with cosine similarity thresholding (`High > 0.65`, `Medium > 0.40`, `Low`), equipped with automated TF-IDF fallback for CPU environments.

---

## 3. Engineering Decisions & Trade-Offs

### 1. Offline-First vs. Cloud LLM APIs
* **Decision**: All NLP components run locally on CPU without external API calls.
* **Trade-off**: Slightly lower conversational flexibility compared to GPT-4, but provides **zero operational cost**, **sub-second latency**, **100% data privacy**, and **guaranteed availability without cloud rate-limits**.

### 2. Extractive vs. Generative Summarization
* **Decision**: Sentences are scored and selected directly from source text using TF-IDF term weights.
* **Trade-off**: Extractive summaries preserve exact factual claims (financial numbers, legal dates, employee names) with **zero hallucination risk**, which is mandatory for enterprise compliance.

### 3. Abstract Factory vs. Ad-hoc Parsers
* **Decision**: All document parsers inherit from `BaseProcessor` and are instantiated via `get_processor()`.
* **Trade-off**: Cleaner code organization and easy extensibility—adding new file formats (e.g. Markdown or RTF) requires only adding a new processor class without touching orchestrator logic.
