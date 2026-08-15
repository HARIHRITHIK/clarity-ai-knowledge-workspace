"""
Text and CSV processor.
For .txt — returns the raw text (cleaned).
For .csv — converts to a human-readable prose representation so the
           same summarisation and entity-extraction pipeline can run on it.
"""

import io
from processors.base import BaseProcessor


class TextProcessor(BaseProcessor):
    """Handles plain-text and CSV files."""

    def extract_text(self, file_path: str, raw_bytes: bytes) -> str:
        ext = file_path.rsplit(".", 1)[-1].lower()
        if ext == "csv":
            return self._extract_csv(raw_bytes)
        return self._extract_text(raw_bytes)

    # ── Private ───────────────────────────────────────────────────────────────

    def _extract_text(self, raw_bytes: bytes) -> str:
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                text = raw_bytes.decode(encoding)
                return self.clean(text)
            except UnicodeDecodeError:
                continue
        return self.clean(raw_bytes.decode("utf-8", errors="replace"))

    def _extract_csv(self, raw_bytes: bytes) -> str:
        """
        Convert CSV to a prose summary so the NLP pipeline works normally.
        Reads headers + rows and formats them as 'Column: Value' sentences.
        """
        try:
            import pandas as pd
            df = pd.read_csv(io.BytesIO(raw_bytes), nrows=200)

            lines = [f"Data contains {len(df)} rows and {len(df.columns)} columns."]
            lines.append(f"Columns: {', '.join(df.columns.tolist())}.\n")

            # Produce a prose row for each record
            for _, row in df.head(50).iterrows():
                parts = []
                for col in df.columns:
                    val = row[col]
                    if pd.notna(val) and str(val).strip():
                        parts.append(f"{col}: {val}")
                if parts:
                    lines.append(". ".join(parts) + ".")

            return self.clean("\n".join(lines))
        except Exception:
            # Fall back to raw text if pandas fails
            return self._extract_text(raw_bytes)
