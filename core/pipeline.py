"""
Processing pipeline orchestrator.

Coordinates the full document processing lifecycle:
  Parse → Classify → Summarize → Extract Entities → Embed → Index

Each stage is isolated so failures in one stage do not block the others.
New stages can be added without touching the caller.
"""

from __future__ import annotations
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from core.document import Document
from core.workspace import Workspace
from processors.base import get_processor
from intelligence.classifier import DocumentClassifier
from intelligence.summarizer import Summarizer
from intelligence.extractor import EntityExtractor
from intelligence.search import embed_text
import config


class Pipeline:
    """
    Runs every document through the processing stages in order.

    Usage:
        pipeline = Pipeline()
        doc = pipeline.run(filename, raw_bytes, on_progress=callback)
        Workspace.add(doc)
    """

    def __init__(self):
        self.classifier = DocumentClassifier()
        self.summarizer = Summarizer()
        self.extractor  = EntityExtractor()

    def run(
        self,
        filename:    str,
        raw_bytes:   bytes,
        on_progress: Optional[Callable[[str, int], None]] = None,
        is_demo:     bool = False,
    ) -> Document:
        """
        Process a document through all pipeline stages.

        Args:
            filename:    Original filename including extension.
            raw_bytes:   File content as bytes.
            on_progress: Optional callback(stage_name, pct_complete).
            is_demo:     Tag document as demo content.

        Returns:
            Fully processed Document. On error, document.processing_error is set.
        """

        def _progress(stage: str, pct: int):
            if on_progress:
                on_progress(stage, pct)

        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"
        doc = Document(filename=filename, file_type=ext, is_demo=is_demo)

        try:
            # ── Stage 1: Parse ─────────────────────────────────────────────
            _progress("Parsing document", 10)
            processor = get_processor(ext)
            content   = processor.extract_text(filename, raw_bytes)

            if not content.strip():
                doc.processing_error = "No readable text found in this file."
                return doc

            # Truncate very large documents to keep processing fast
            if len(content) > config.MAX_CONTENT_CHARS:
                content = content[: config.MAX_CONTENT_CHARS]

            doc.content    = content
            doc.word_count = len(content.split())
            doc.char_count = len(content)

            # ── Stage 2: Classify ──────────────────────────────────────────
            _progress("Classifying document", 30)
            category, _conf = self.classifier.classify(content)
            doc.category = category

            # ── Stage 3: Summarise ─────────────────────────────────────────
            _progress("Generating summary", 50)
            doc.summary   = self.summarizer.summarize(content)
            doc.key_facts = self.summarizer.key_facts(content)

            # ── Stage 4: Extract entities ──────────────────────────────────
            _progress("Extracting entities", 70)
            doc.entities = self.extractor.extract(content)

            # ── Stage 5: Embed for search ──────────────────────────────────
            _progress("Building search index", 90)
            index_text   = f"{doc.summary} {' '.join(doc.key_facts)}"
            doc.embedding = embed_text(index_text)

            # ── Done ───────────────────────────────────────────────────────
            _progress("Complete", 100)
            doc.processed_at = datetime.now()
            doc.is_processed  = True

        except Exception as exc:
            doc.processing_error = str(exc)

        return doc

    def run_from_path(self, path: str, is_demo: bool = False) -> Document:
        """Convenience method for loading documents from disk (demo workspace)."""
        p = Path(path)
        if not p.exists():
            doc = Document(filename=p.name, file_type="txt")
            doc.processing_error = f"File not found: {path}"
            return doc
        return self.run(
            filename  = p.name,
            raw_bytes = p.read_bytes(),
            is_demo   = is_demo,
        )
