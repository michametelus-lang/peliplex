"""Convert beat-scene matches into an edit timeline."""
from __future__ import annotations

from typing import List

from models import SceneMatch, TimelineItem


class TimelinePlanner:
    """Build timeline items with smooth pacing and context windows."""

    def plan(self, matches: List[SceneMatch], intensity: str) -> List[TimelineItem]:
        items: List[TimelineItem] = []
        intensity_factor = {"baja": 1.15, "media": 1.0, "alta": 0.85}[intensity]

        for m in matches:
            desired = max(2.0, m.beat.target_duration * intensity_factor / max(0.8, m.beat.intensity_weight))
            source_dur = m.scene.end - m.scene.start
            clip_dur = min(source_dur, desired)

            # expand context slightly for setup/resolution to avoid abrupt flow
            context_pad = 0.5 if m.beat.beat_type in {"setup", "resolution"} else 0.2
            clip_start = max(0.0, m.scene.start - context_pad)
            clip_end = max(clip_start + 2.0, min(m.scene.end + context_pad, clip_start + clip_dur))

            items.append(
                TimelineItem(
                    beat_type=m.beat.beat_type,
                    source_start=m.scene.start,
                    source_end=m.scene.end,
                    clip_start=round(clip_start, 3),
                    clip_end=round(clip_end, 3),
                    narration_text=m.beat.text,
                )
            )

        items.sort(key=lambda x: x.clip_start)
        return items
