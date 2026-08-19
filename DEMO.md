> **Live Demo:** [https://clarity-ai-knowledge-workspace-ctubssksgzly4wrfbcz6pn.streamlit.app/](https://clarity-ai-knowledge-workspace-ctubssksgzly4wrfbcz6pn.streamlit.app/)

---

# 2-Minute Recruiter Demo

This guide provides a deterministic, **2-minute evaluation walkthrough** of **Clarity — AI Knowledge Workspace**.

---

### Step 1: Open Live Demo
Open the live deployment link above or run the app locally:
```bash
streamlit run app.py
```

### Step 2: Load Sample Document Corpus
* On the **Home** landing page, click **`🚀 Open Demo Workspace`** (or go to **Upload** and upload files from `sample_data/`).
* The system automatically queues the pre-bundled multi-format enterprise dataset (`company_report.pdf`, `employee_policy.docx`, `project_notes.txt`, `sales_summary.csv`).

### Step 3: Process the Corpus
* Watch the **5-stage NLP pipeline** execute with live progress updates:
  ```
  Text Parsing ➔ Domain Classification ➔ Extractive Summarization ➔ Named Entity Recognition ➔ Semantic Indexing
  ```

### Step 4: Review Classification
* Navigate to the **Dashboard**.
* Review the **Workspace Health** metrics:
  * Total Documents & Word Counts
  * Auto-Detected Domain Categories (e.g. *Financial Report*, *HR Policy*, *Meeting Notes*, *Contract / Legal*)
  * Interactive Plotly distribution donut and horizontal bar charts

### Step 5: Review Extractive Summary
* In the **Document Library**, click **`View →`** on any document (e.g., `Acme Q4 Financial Report`).
* Under the **Summary** tab, review the 4-sentence extractive executive summary and numbered key facts generated via TF-IDF sentence matrix scoring.

### Step 6: Inspect Entities (NER)
* Switch to the **Entities** tab.
* Inspect extracted entity chips organized by type:
  * 👤 **People** (e.g. *Sarah Rodriguez*, *Michael Chen*, *David Kim*)
  * 🏢 **Organizations** (e.g. *TechSupply Solutions*, *Meridian Financial*)
  * 📅 **Dates** (e.g. *January 15, 2025*, *Q4 2024*)
  * 💰 **Amounts** (e.g. *$24.7 million*, *$180,000*)
  * 📍 **Locations** (e.g. *Austin*)

### Step 7: Perform Semantic Search
* Click **Search** in the sidebar.
* Test natural language business queries:
  * `"quarterly revenue and financial profit"`
  * `"employee remote work and vacation policy"`
  * `"David Kim engineering architecture"`
* Observe relevance ranking with **High / Medium / Low** confidence indicators and contextual matching excerpts.

### Step 8: Generate Executive Report
* Navigate to **Reports**.
* Click **`✓ Select All`** and click **`📄 Generate Report`**.
* Review the in-app executive summary and click **`⬇️ Download HTML Report`** to export a standalone, print-ready HTML document.
