"""Heuristic style detector for dominant narrative category."""
from __future__ import annotations

from collections import Counter
from typing import Dict, List

from models import StylePrediction, TranscriptSegment


STYLE_KEYWORDS: Dict[str, List[str]] = {
    "accion": ["corre", "explota", "persecución", "escapa", "lucha"],
    "drama": ["familia", "decisión", "secreto", "culpa", "pérdida"],
    "terror": ["oscuro", "miedo", "sombra", "grito", "pesadilla"],
    "misterio": ["pista", "desaparece", "pregunta", "enigma", "investiga"],
    "romance": ["amor", "mirada", "promesa", "beso", "corazón"],
}


class StyleDetector:
    """Infer dominant style from transcript keyword density."""

    def predict(self, segments: List[TranscriptSegment]) -> StylePrediction:
        text = " ".join(s.text.lower() for s in segments)
        counts = Counter()
        for style, words in STYLE_KEYWORDS.items():
            counts[style] = sum(text.count(w) for w in words)
        total = sum(counts.values()) or 1
        scores = {k: v / total for k, v in counts.items()}
        primary = max(scores, key=scores.get)
        return StylePrediction(primary_style=primary, scores=scores)
