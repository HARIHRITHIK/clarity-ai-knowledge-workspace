# 📸 Clarity Workspace Screenshots

This directory stores the high-resolution UI preview screenshots for the GitHub repository and documentation.

## Expected Files

To display screenshots in the main `README.md`, upload four screenshots corresponding to the core workflow:

1. **`workspace.png`** — Overview of the Dashboard showing Workspace Health metrics (Documents, Categories, People, Organizations, Facts) and Plotly visualization charts.
2. **`document-analysis.png`** — Document detail view displaying the extractive executive summary, numbered key facts, and color-coded entity chips (`PERSON`, `ORG`, `DATE`, `MONEY`, `GPE`).
3. **`semantic-search.png`** — Semantic search interface showing natural language query input, suggestion chips, confidence badges (`High`, `Medium`, `Low`), and context snippets.
4. **`executive-report.png`** — Report Builder preview showing document selection and formatted HTML executive report output.

---

## How to Add / Update Screenshots

1. Take a clean screenshot of the application running locally at `http://localhost:8501`.
2. Name the image file exactly as specified above (e.g., `workspace.png`).
3. Place or upload the file into `assets/screenshots/`.
4. Commit and push your changes to GitHub:
   ```bash
   git add assets/screenshots/
   git commit -m "docs: add application preview screenshots"
   git push origin main
   ```
5. GitHub will automatically render the screenshots inside `README.md`.
