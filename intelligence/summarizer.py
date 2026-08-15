"""
Extractive text summariser — no LLM, no API, fully offline.

Algorithm (LSA-inspired sentence scoring):
  1. Split text into sentences.
  2. Build a TF-IDF matrix over sentences.
  3. Score each sentence by the sum of its TF-IDF weights.
  4. Select the top-N highest-scoring sentences.
  5. Return them in original document order (coherent reading flow).

This is reliable, deterministic, and fast enough to run on every upload.
"""

from __future__ import annotations
import re
from typing import List

import config


def _sentence_split(text: str) -> List[str]:
    """Robust sentence splitter that handles abbreviations reasonably well."""
    # Split on . ! ? followed by whitespace and uppercase or end of string
    pattern = r"(?<=[.!?])\s+(?=[A-Z])"
    sentences = re.split(pattern, text.strip())
    # Also split on newline-separated items (bullet points, numbered lists)
    expanded = []
    for sent in sentences:
        sub = [s.strip() for s in sent.split("\n") if len(s.strip()) > 20]
        expanded.extend(sub if sub else [sent])
    return [s for s in expanded if len(s.split()) >= 5]


def _tfidf_scores(sentences: List[str]) -> List[float]:
    """Return a TF-IDF importance score for each sentence."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

    if len(sentences) < 2:
        return [1.0] * len(sentences)

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        matrix = vectorizer.fit_transform(sentences)
        # Score = sum of TF-IDF weights across all terms in the sentence
        scores = matrix.sum(axis=1).A1.tolist()
        return scores
    except Exception:
        return [1.0] * len(sentences)


class Summarizer:
    """Produces extractive summaries and ranked key-fact sentences."""

    def summarize(self, text: str, n_sentences: int | None = None) -> str:
        """
        Return a coherent extractive summary.

        Args:
            text:        Source document text.
            n_sentences: How many sentences to include. Defaults to config value.
        """
        n = n_sentences or config.SUMMARY_SENTENCE_COUNT
        sentences = _sentence_split(text)

        if not sentences:
            return ""
        if len(sentences) <= n:
            return " ".join(sentences)

        scores = _tfidf_scores(sentences)
        ranked = sorted(
            range(len(sentences)), key=lambda i: scores[i], reverse=True
        )[:n]

        # Return in original order for readability
        selected = sorted(ranked)
        return " ".join(sentences[i] for i in selected)

    def key_facts(self, text: str, n: int | None = None) -> List[str]:
        """
        Return the top-N most information-dense sentences as key facts.
        Distinct from summary: picks slightly more sentences, skips overlap.
        """
        n = n or config.KEY_FACTS_COUNT
        sentences = _sentence_split(text)

        if not sentences:
            return []

        scores = _tfidf_scores(sentences)
        ranked = sorted(
            range(len(sentences)), key=lambda i: scores[i], reverse=True
        )

        facts = []
        seen_tokens: set[str] = set()
        for idx in ranked:
            sent = sentences[idx].strip()
            # Simple deduplication: skip if >50% of words seen before
            tokens = set(sent.lower().split())
            overlap = len(tokens & seen_tokens) / max(len(tokens), 1)
            if overlap < 0.5:
                facts.append(sent)
                seen_tokens.update(tokens)
            if len(facts) >= n:
                break

        return facts
