"""Narrative structure extraction from transcripts and summary."""
from __future__ import annotations

from typing import List

from models import StoryStructure, SummaryResult, TranscriptSegment


class StoryAnalyzer:
    """Build a story structure optimized for short-form narrative videos."""

    def analyze(self, segments: List[TranscriptSegment], summary: SummaryResult) -> StoryStructure:
        text_chunks = [s.text.strip() for s in segments if s.text.strip()]
        if not text_chunks:
            text_chunks = [summary.summary_text]

        n = len(text_chunks)
        q1 = text_chunks[0]
        q2 = text_chunks[min(1, n - 1)]
        mid = text_chunks[n // 2]
        pre_end = text_chunks[max(0, n - 2)]
        end = text_chunks[-1]

        return StoryStructure(
            hook=f"Nadie esperaba esto: {q1[:100]}",
            setup=q2[:150],
            conflict=mid[:170],
            twist=summary.highlights[0] if summary.highlights else pre_end[:150],
            climax=pre_end[:170],
            resolution=end[:150],
        )
        
