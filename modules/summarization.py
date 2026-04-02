"""Summarization module with chunking support."""
from __future__ import annotations

import logging
from typing import List

from models import SummaryResult, TranscriptSegment
from utils import normalize_text

logger = logging.getLogger(__name__)


class Summarizer:
    """Create structured summaries from transcript segments."""

    def __init__(self, max_chunk_chars: int = 1800) -> None:
        self.max_chunk_chars = max_chunk_chars

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks: List[str] = []
        current = []
        size = 0
        for w in words:
            size += len(w) + 1
            current.append(w)
            if size >= self.max_chunk_chars:
                chunks.append(" ".join(current))
                current, size = [], 0
        if current:
            chunks.append(" ".join(current))
        return chunks

    def _neutral_summary(self, chunks: List[str]) -> str:
        return " ".join([" ".join(chunk.split()[:45]) for chunk in chunks[:4]])

    def _viral_style(self, base: str) -> str:
        intro = "Lo que empieza normal se transforma rápido:"
        return f"{intro} {base}" if base else intro

    def summarize(self, segments: List[TranscriptSegment], mode: str = "viral_story") -> SummaryResult:
        """Generate a structured summary for downstream narrative modules."""
        full_text = normalize_text(" ".join(s.text for s in segments))
        chunks = self._chunk_text(full_text)
        neutral = self._neutral_summary(chunks)
        summary_text = self._viral_style(neutral) if mode == "viral_story" else neutral

        key_points = [" ".join(c.split()[:18]) for c in chunks[:6] if c]
        highlights = [kp for kp in key_points if len(kp.split()) > 6][:4]
        logger.info("Resumen generado en modo %s", mode)
        return SummaryResult(
            mode=mode,
            summary_text=summary_text,
            key_points=key_points,
            highlights=highlights,
        )
