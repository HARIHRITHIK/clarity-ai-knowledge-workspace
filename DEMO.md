# 🎯 Clarity — Recruiter & Interview Demo Guide

This guide provides a **reproducible 2-minute walkthrough** of the core capabilities of **Clarity**.

---

## ⚡ Quick Demo (2-Minute Walkthrough)

### 1. Launch Clarity
Run the application locally or open the live deployment:
```bash
streamlit run app.py
```

### 2. Load the Demo Corpus
* On the **Home** screen, click **`🚀 Open Demo Workspace`**.
* Watch the 5-stage automated pipeline process 5 realistic Acme Corporation documents in real-time with per-stage progress indicators (`Parse` ➔ `Classify` ➔ `Summarize` ➔ `Extract Entities` ➔ `Build Index`).

### 3. Explore Workspace Health Metrics
* Navigate to the **Dashboard**.
* Review the aggregated enterprise health metrics:
  - **Documents** (5)
  - **Categories** (5 auto-detected types)
  - **People Mentioned** (Extracted named individuals)
  - **Key Facts** (Extracted business statements)
  - **Search Coverage** (100%)
* Inspect the interactive **Category Distribution** donut chart and **Document Size** bar chart.

### 4. Inspect Extracted Document Intelligence
* In the **Document Library**, click **`View →`** on `Acme Q4 2024 Financial Report`.
* **Summary Tab**: Review the 4-sentence extractive executive summary and numbered key facts.
* **Entities Tab**: Review color-coded chips for **People**, **Organizations**, **Dates**, and **Amounts** along with the frequency table.
* **Export Tab**: Download the document's structured data as `JSON` or `CSV`.

### 5. Perform Semantic Search
* Click **Search** in the sidebar.
* Try natural language queries or click one of the quick suggestions:
  - `"quarterly revenue and financial profit"`
  - `"Sarah Rodriguez"`
  - `"remote work policy"`
* Note the **High / Medium / Low** confidence ranking badges and query match excerpts.

### 6. Generate an Executive HTML Report
* Navigate to **Reports**.
* Click **`✓ Select All`** (or pick specific documents).
* Click **`📄 Generate Report`** to preview the in-app executive summary.
* Click **`⬇️ Download HTML Report`** to export a standalone, print-ready HTML document.

---

## 📁 Testing Manual Uploads

A multi-format test corpus is provided in `sample_data/`:
* `company_report.pdf` — Multi-page PDF financial report
* `employee_policy.docx` — Microsoft Word HR policy handbook
* `project_notes.txt` — Plain text engineering sprint minutes
* `sales_summary.csv` — Tabular customer sales records

To test manual processing:
1. Navigate to **Upload**.
2. Drag and drop any file from `sample_data/`.
3. Click **`⚡ Process Documents`**.
