"""
In-memory workspace manager built on Streamlit session state.
Acts as a lightweight repository layer — the rest of the application
talks to Workspace, not to st.session_state directly.
Swapping to SQLite or Postgres in v2 only requires changing this module.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set
import streamlit as st

from core.document import Document, Entity
import config


class Workspace:
    """
    Manages all documents for the current browser session.
    Every method is a static accessor to session_state so callers
    do not need to hold a Workspace instance.
    """

    # ── Initialisation ────────────────────────────────────────────────────────

    @staticmethod
    def init() -> None:
        """Call once at app startup to ensure all keys exist."""
        defaults = {
            "documents":       {},          # Dict[str, Document]
            "workspace_name":  "My Workspace",
            "current_doc_id":  None,
            "current_page":    "home",
            "search_query":    "",
            "demo_loaded":     False,
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    # ── CRUD ──────────────────────────────────────────────────────────────────

    @staticmethod
    def add(doc: Document) -> str:
        st.session_state.documents[doc.id] = doc
        return doc.id

    @staticmethod
    def get(doc_id: str) -> Optional[Document]:
        return st.session_state.documents.get(doc_id)

    @staticmethod
    def remove(doc_id: str) -> None:
        st.session_state.documents.pop(doc_id, None)
        if st.session_state.current_doc_id == doc_id:
            st.session_state.current_doc_id = None

    @staticmethod
    def clear() -> None:
        st.session_state.documents = {}
        st.session_state.demo_loaded = False
        st.session_state.current_doc_id = None

    # ── Queries ───────────────────────────────────────────────────────────────

    @staticmethod
    def all() -> List[Document]:
        return list(st.session_state.documents.values())

    @staticmethod
    def processed() -> List[Document]:
        return [d for d in Workspace.all() if d.is_processed]

    @staticmethod
    def count() -> int:
        return len(st.session_state.documents)

    @staticmethod
    def is_empty() -> bool:
        return Workspace.count() == 0

    @staticmethod
    def get_by_category(category: str) -> List[Document]:
        return [d for d in Workspace.processed() if d.category == category]

    # ── Aggregate Stats (Workspace Health) ───────────────────────────────────

    @staticmethod
    def stats() -> Dict:
        """
        Compute workspace health metrics displayed on the dashboard.
        """
        docs = Workspace.all()
        proc = Workspace.processed()

        people:        Set[str] = set()
        orgs:          Set[str] = set()
        categories:    Set[str] = set()
        total_facts:   int      = 0

        for doc in proc:
            categories.add(doc.category)
            total_facts += len(doc.key_facts)
            for entity in doc.entities.get("PERSON", []):
                people.add(entity.text.title())
            for entity in doc.entities.get("ORG", []):
                orgs.add(entity.text.title())

        search_pct = 100 if proc else 0

        return {
            "total_documents":    len(docs),
            "processed_documents": len(proc),
            "categories":         len(categories),
            "people_mentioned":   len(people),
            "organizations":      len(orgs),
            "key_facts":          total_facts,
            "search_coverage":    search_pct,
            "total_words":        sum(d.word_count for d in proc),
        }

    @staticmethod
    def all_entities() -> Dict[str, List[str]]:
        """Union of all entities across the workspace, deduplicated."""
        result: Dict[str, Set[str]] = {
            "PERSON": set(), "ORG": set(), "DATE": set(),
            "MONEY": set(), "GPE": set(),
        }
        for doc in Workspace.processed():
            for label, entities in doc.entities.items():
                if label in result:
                    for e in entities:
                        result[label].add(e.text.title())
        return {k: sorted(v) for k, v in result.items()}

    # ── Navigation ────────────────────────────────────────────────────────────

    @staticmethod
    def navigate(page: str, doc_id: Optional[str] = None) -> None:
        st.session_state.current_page = page
        if doc_id is not None:
            st.session_state.current_doc_id = doc_id

    @staticmethod
    def current_page() -> str:
        return st.session_state.get("current_page", "home")
