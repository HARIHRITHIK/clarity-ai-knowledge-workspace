"""
Semantic search engine.

Primary:  sentence-transformers (all-MiniLM-L6-v2)
Fallback: TF-IDF + cosine similarity via scikit-learn

On machines where PyTorch/torch DLLs fail to load (common on Windows),
the model load is attempted in a background thread with a 15-second
timeout. After one failed attempt the app permanently uses TF-IDF —
no UI freeze, no repeated DLL errors, graceful degradation.

Confidence bands replace raw scores:
  >= 0.65 -> High
  >= 0.40 -> Medium
  <  0.40 -> Low
"""

from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import List, Optional
import numpy as np

import config


# ── Model state ───────────────────────────────────────────────────────────────

_model       = None
_st_available = False
_load_tried  = False          # Once False->True we never retry (avoids DLL spam)
_load_lock   = threading.Lock()


def _attempt_load() -> bool:
    """
    Try to load sentence-transformers in a daemon thread.
    Returns True if model loaded successfully within the timeout.
    """
    global _model, _st_available

    success = threading.Event()

    def _do_load():
        global _model, _st_available
        try:
            from sentence_transformers import SentenceTransformer
            m = SentenceTransformer("all-MiniLM-L6-v2")
            _model = m
            _st_available = True
            success.set()
        except Exception:
            pass
        finally:
            success.set()   # Always unblock the waiter

    t = threading.Thread(target=_do_load, daemon=True)
    t.start()
    success.wait(timeout=15)   # Never hang longer than 15 s

    return _st_available


def _load_model():
    """
    Return (model, available). Tries exactly once; subsequent calls return
    cached result immediately — avoids repeated DLL init attempts.
    """
    global _load_tried
    with _load_lock:
        if not _load_tried:
            _load_tried = True
            _attempt_load()
    return _model, _st_available


# ── Result type ───────────────────────────────────────────────────────────────

@dataclass
class SearchResult:
    doc_id:     str
    filename:   str
    category:   str
    excerpt:    str
    score:      float
    confidence: str     # "High" | "Medium" | "Low"


def _score_to_confidence(score: float) -> str:
    if score >= config.CONFIDENCE_HIGH:
        return "High"
    if score >= config.CONFIDENCE_MEDIUM:
        return "Medium"
    return "Low"


def _best_excerpt(text: str, query: str, window: int = 300) -> str:
    """Extract the most relevant passage for display."""
    lower        = text.lower()
    query_words  = [w.lower() for w in query.split() if len(w) > 2]
    best_pos, best_hits = 0, 0

    for i in range(0, len(text), 50):
        snippet = lower[i : i + window]
        hits    = sum(snippet.count(w) for w in query_words)
        if hits > best_hits:
            best_hits, best_pos = hits, i

    excerpt = text[best_pos : best_pos + window].strip()
    if best_pos > 0:
        excerpt = "…" + excerpt
    if best_pos + window < len(text):
        excerpt += "…"
    return excerpt or text[:window]


# ── TF-IDF fallback ───────────────────────────────────────────────────────────

def _tfidf_search(query: str, documents: list, top_k: int) -> List[SearchResult]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as sk_cos

    corpus = [f"{d.summary} {' '.join(d.key_facts)}" for d in documents]
    if not corpus:
        return []
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix     = vectorizer.fit_transform(corpus + [query])
        scores     = sk_cos(matrix[-1], matrix[:-1]).flatten()
    except Exception:
        return []

    ranked  = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in ranked:
        score = float(scores[idx])
        if score < 0.01:
            continue
        doc = documents[idx]
        # Re-scale TF-IDF scores (typically 0–0.5) to match confidence thresholds
        adj_score = min(score * 2.0, 1.0)
        results.append(SearchResult(
            doc_id=doc.id,
            filename=doc.filename,
            category=doc.category,
            excerpt=_best_excerpt(doc.content, query),
            score=round(score, 3),
            confidence=_score_to_confidence(adj_score),
        ))
    return results


# ── Embedding helpers (used by pipeline) ─────────────────────────────────────

def embed_text(text: str) -> Optional[List[float]]:
    """
    Encode text to a dense vector.
    Returns None if sentence-transformers is unavailable — the pipeline
    continues without an embedding (TF-IDF search still works).
    """
    model, available = _load_model()
    if not available or model is None:
        return None
    try:
        vec = model.encode(text[:2048], normalize_embeddings=True)
        return vec.tolist()
    except Exception:
        return None


def cosine_similarity(a: List[float], b: List[float]) -> float:
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    return float(np.dot(va, vb) / denom) if denom else 0.0


# ── Public search API ─────────────────────────────────────────────────────────

class SearchEngine:
    """Workspace-wide semantic search with automatic TF-IDF fallback."""

    def search(self, query: str, documents: list) -> List[SearchResult]:
        if not query.strip() or not documents:
            return []

        docs_with_embeddings = [d for d in documents if d.embedding is not None]

        if docs_with_embeddings:
            return self._semantic_search(query, documents, docs_with_embeddings)

        return _tfidf_search(query, documents, config.SEARCH_TOP_K)

    def _semantic_search(
        self, query: str, all_docs: list, embedded_docs: list
    ) -> List[SearchResult]:
        model, available = _load_model()
        results = []

        if available and model is not None:
            try:
                q_vec = model.encode(query, normalize_embeddings=True).tolist()
                for doc in embedded_docs:
                    score = cosine_similarity(q_vec, doc.embedding)
                    results.append(SearchResult(
                        doc_id=doc.id,
                        filename=doc.filename,
                        category=doc.category,
                        excerpt=_best_excerpt(doc.content, query),
                        score=round(score, 3),
                        confidence=_score_to_confidence(score),
                    ))
                # Also search docs that missed embedding (TF-IDF)
                docs_no_emb = [d for d in all_docs if d.embedding is None]
                if docs_no_emb:
                    results.extend(_tfidf_search(query, docs_no_emb, config.SEARCH_TOP_K))
            except Exception:
                results = _tfidf_search(query, all_docs, config.SEARCH_TOP_K)
        else:
            results = _tfidf_search(query, all_docs, config.SEARCH_TOP_K)

        results.sort(key=lambda r: r.score, reverse=True)
        return results[: config.SEARCH_TOP_K]

    @property
    def engine_name(self) -> str:
        _, available = _load_model()
        return "Semantic (sentence-transformers)" if available else "Keyword (TF-IDF)"
