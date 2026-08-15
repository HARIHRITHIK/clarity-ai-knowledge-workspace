"""
Document type classifier.

Uses TF-IDF keyword scoring against curated category keyword sets.
Deterministic, fully offline, no model required, instant.

Design note: This is intentionally simple.  A weighted keyword classifier
is explainable, testable, and reliable — the right tool for category
detection on structured business documents.  An LLM would add latency,
cost, and opacity with no measurable quality gain for this task.
"""

from __future__ import annotations
from typing import Tuple
import re

import config


class DocumentClassifier:
    """Assigns one of the configured categories to a document."""

    def classify(self, text: str) -> Tuple[str, float]:
        """
        Score the document against every category keyword list.

        Returns:
            (category_name, confidence_score)
        """
        if not text:
            return "General", 0.0

        lower_text = text.lower()
        words       = re.findall(r"\b\w+\b", lower_text)
        word_count  = max(len(words), 1)

        scores: dict[str, float] = {}
        for category, keywords in config.CATEGORY_KEYWORDS.items():
            hits = 0
            for kw in keywords:
                # Count overlapping occurrences of the keyword phrase
                hits += lower_text.count(kw.lower())
            # Normalise by document length (hits per 1000 words)
            scores[category] = (hits / word_count) * 1000

        if not scores or max(scores.values()) == 0:
            return "General", 0.0

        best_category  = max(scores, key=scores.__getitem__)
        best_score     = scores[best_category]

        # Map raw score to 0–1 confidence (soft cap at 10 hits/1000 words = 1.0)
        confidence = min(best_score / 10.0, 1.0)

        return best_category, round(confidence, 3)
