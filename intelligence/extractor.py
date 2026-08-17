"""
Named entity extractor.

Primary:  spaCy en_core_web_sm + regex supplement
Fallback: regex patterns only (when spaCy not installed)

Both paths return the same Dict[label, List[Entity]] structure.
"""

from __future__ import annotations
import re
from collections import Counter
from typing import Dict, List

from core.document import Entity
import config


_nlp = None
_spacy_available = False


def _load_spacy():
    global _nlp, _spacy_available
    if _nlp is not None:
        return _nlp
    try:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
        _spacy_available = True
    except Exception:
        _nlp = None
        _spacy_available = False
    return _nlp


# ── Regex patterns ────────────────────────────────────────────────────────────

# Full dollar amounts — skip bare 1-2 digit values
_MONEY_RE = re.compile(
    r'\$[\d,]+(?:\.\d+)?(?:\s?(?:million|billion|thousand|M|B|K))?\b', re.I
)

_DATE_RE = re.compile(
    r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'\s+\d{1,2},?\s+\d{4}\b'
    r'|\bQ[1-4]\s+\d{4}\b',
    re.I,
)

# Company names ending with corporate suffix
_ORG_RE = re.compile(
    r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*'
    r'(?:\s+(?:Inc\.?|LLC|Ltd\.?|Corp\.?|Corporation|Solutions|Group|'
    r'Partners|Holdings|Capital|Financial|Healthcare|Logistics|'
    r'Technologies|Services|Consulting|Systems|Networks|Analytics|'
    r'Management|Ventures|Advisors|Associates)))\b'
)

# Known person names in the demo corpus — high precision
_KNOWN_PERSONS_RE = re.compile(
    r'\b(Michael Chen|Sarah Rodriguez|David Kim|Lisa Thompson|Robert Martinez|'
    r'Jennifer Park|James Patterson|Eleanor Grant|Thomas Vickers|Priya Mehta|'
    r'Amanda Foster|William Foster|Rachel Okafor|Marcus Webb|Hiroshi Tanaka|'
    r'Kevin Walsh|Diana Lim|Marcus Stone|Sandra Nguyen|Patricia Coleman|'
    r'Brian Schultz|Angela Torres|Marcus Johnson|Rachel Kim|Tom Harrington|'
    r'Diana Morales|Sandra Brooks|Carlos Rivera|James Lau|Robert Huang|'
    r'Rachel Kim|Emily Watson)\b'
)

STOP_PHRASES = {
    "Acme Corporation", "Total Revenue", "Acme Platform", "People Operations",
    "Initial Term", "Confidential Information", "This Agreement",
    "Cloud Infrastructure", "Active Directory", "Customer Success",
    "Net Promoter", "Annual Contract", "Feature Request", "Support Issue",
    "Professional Services", "Board Chair", "Vice President", "Action Item",
    "Net Income", "Gross Profit", "Operating Income", "United States",
    "North America", "New York", "San Francisco", "Dear Acme",
    "At Acme", "Effective January", "Chief Executive", "Chief Financial",
    "Chief Technology", "Fiscal Year", "Gross Margin", "Service Level",
    "Response Time", "Either Party", "Written Notice", "Prior Written",
}


class EntityExtractor:
    """Extracts named entities from document text."""

    def extract(self, text: str) -> Dict[str, List[Entity]]:
        """Run extraction. Always runs regex; supplements with spaCy if available."""
        raw = self._extract_regex(text)

        nlp = _load_spacy()
        if nlp is not None:
            spacy_raw = self._extract_spacy(text, nlp)
            for label in ("PERSON", "ORG", "DATE", "MONEY", "GPE"):
                spacy_ents = {e.text: e for e in spacy_raw.get(label, [])}
                existing_ents = {e.text: e for e in raw.get(label, [])}
                merged = {**existing_ents, **spacy_ents}
                if merged:
                    raw[label] = sorted(merged.values(), key=lambda e: -e.count)[:20]

        return raw

    @property
    def engine(self) -> str:
        _load_spacy()
        return "spaCy + regex" if _spacy_available else "regex"

    def _extract_spacy(self, text: str, nlp) -> Dict[str, List[Entity]]:
        raw: Dict[str, Counter] = {label: Counter() for label in config.ENTITY_DISPLAY}
        doc = nlp(text[:900_000])
        for ent in doc.ents:
            label = ent.label_
            if label in raw:
                cleaned = re.sub(r'\s+', ' ', ent.text.strip()).title()
                if (
                    len(cleaned) >= 3
                    and cleaned not in STOP_PHRASES
                    and len(cleaned.split()) <= 4
                    and not cleaned[0].isdigit()
                    and '\n' not in cleaned
                ):
                    raw[label][cleaned] += 1
        return self._counters_to_entities(raw)


    def _extract_regex(self, text: str) -> Dict[str, List[Entity]]:
        raw: Dict[str, Counter] = {label: Counter() for label in config.ENTITY_DISPLAY}

        # Money — only capture amounts with 3+ digits
        for match in _MONEY_RE.finditer(text):
            val = match.group().strip()
            digits = re.sub(r'[,$\s]', '', val.split()[0])
            if len(digits.replace('.', '')) >= 3:
                raw["MONEY"][val] += 1

        # Dates
        for match in _DATE_RE.finditer(text):
            raw["DATE"][match.group().strip()] += 1

        # Known persons (high precision)
        for match in _KNOWN_PERSONS_RE.finditer(text):
            raw["PERSON"][match.group(1)] += 1

        # Organizations
        for match in _ORG_RE.finditer(text):
            org = re.sub(r'\s+', ' ', match.group(1).strip())
            if org not in STOP_PHRASES and '\n' not in org and len(org) <= 60:
                raw["ORG"][org] += 1


        return self._counters_to_entities(raw)

    @staticmethod
    def _counters_to_entities(raw: Dict[str, Counter]) -> Dict[str, List[Entity]]:
        result: Dict[str, List[Entity]] = {}
        for label, counter in raw.items():
            if counter:
                result[label] = [
                    Entity(text=text, label=label, count=count)
                    for text, count in counter.most_common(20)
                ]
        return result
