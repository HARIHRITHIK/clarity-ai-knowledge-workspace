"""
Core document data model.
All intelligence layers produce and consume this single structure,
keeping the pipeline composable and the data model stable.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid


@dataclass
class Entity:
    """A single named entity extracted from a document."""
    text: str
    label: str          # PERSON | ORG | DATE | MONEY | GPE
    count: int = 1

    def __hash__(self):
        return hash((self.text.lower(), self.label))

    def __eq__(self, other):
        return (
            isinstance(other, Entity)
            and self.text.lower() == other.text.lower()
            and self.label == other.label
        )


@dataclass
class Document:
    """
    Represents a single processed document in the workspace.

    Fields are populated progressively through the processing pipeline:
    1.  Raw extraction  → filename, file_type, content, word_count, char_count
    2.  Classification  → category
    3.  Summarisation   → summary, key_facts
    4.  Entity extract  → entities
    5.  Embedding       → embedding (enables semantic search)
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    filename: str = ""
    file_type: str = ""          # pdf | docx | txt | csv

    # ── Raw content ───────────────────────────────────────────────────────────
    content: str = ""
    word_count: int = 0
    char_count: int = 0

    # ── Intelligence outputs ──────────────────────────────────────────────────
    category: str = "General"
    summary: str = ""
    key_facts: List[str] = field(default_factory=list)
    entities: Dict[str, List[Entity]] = field(default_factory=dict)
    embedding: Optional[List[float]] = None

    # ── Metadata ──────────────────────────────────────────────────────────────
    processed_at: Optional[datetime] = None
    processing_error: Optional[str] = None
    is_processed: bool = False
    is_demo: bool = False

    # ── Computed helpers ──────────────────────────────────────────────────────
    @property
    def display_name(self) -> str:
        """Clean display name without extension."""
        name = self.filename
        for ext in (".pdf", ".docx", ".txt", ".csv"):
            name = name.replace(ext, "")
        return name.replace("_", " ").replace("-", " ").title()

    @property
    def entity_count(self) -> int:
        return sum(len(v) for v in self.entities.values())

    @property
    def all_people(self) -> List[str]:
        return [e.text for e in self.entities.get("PERSON", [])]

    @property
    def all_orgs(self) -> List[str]:
        return [e.text for e in self.entities.get("ORG", [])]

    @property
    def has_error(self) -> bool:
        return self.processing_error is not None

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to plain dict for export."""
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "category": self.category,
            "word_count": self.word_count,
            "summary": self.summary,
            "key_facts": self.key_facts,
            "entities": {
                label: [{"text": e.text, "count": e.count} for e in ents]
                for label, ents in self.entities.items()
            },
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
        }
