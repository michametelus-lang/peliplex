"""Convert beat-scene matches into an edit timeline with target duration control."""
from __future__ import annotations

from typing import List

from models import SceneMatch, TimelineItem


class TimelinePlanner:
    """Build timeline items with smooth pacing and strict duration targeting."""

    _BEAT_WEIGHT = {
        "hook": 1.0,
        "setup": 0.9,
        "conflict": 1.05,
        "twist": 0.95,
        "climax": 1.2,
        "resolution": 0.9,
    }

    def _intensity_factor(self, intensity: str) -> float:
        return {"baja": 1.18, "media": 1.0, "alta": 0.82}[intensity]

    def plan(self, matches: List[SceneMatch], intensity: str, target_duration: int) -> List[TimelineItem]:
        """Distribute total duration across narrative beats and keep coherent pacing."""
        if not matches:
            return []

        intensity_factor = self._intensity_factor(intensity)
        weighted = [self._BEAT_WEIGHT.get(m.beat.beat_type, 1.0) * max(0.7, m.narrative_match_score) for m in matches]
        total_weight = sum(weighted) or 1.0

        requests: List[float] = []
        max_avail: List[float] = []
        min_clip = 2.0

        for idx, match in enumerate(matches):
            share = weighted[idx] / total_weight
            requested = (target_duration * share) * intensity_factor
            span = max(min_clip, match.scene.end - match.scene.start)
            context = 0.8 if match.beat.beat_type in {"setup", "resolution"} else 0.35
            max_available = max(min_clip, span + context)
            requests.append(max(min_clip, requested))
            max_avail.append(max_available)

        durations = [min(req, limit) for req, limit in zip(requests, max_avail)]
        current_total = sum(durations)

        if current_total > target_duration:
            excess = current_total - target_duration
            shrinkable = [max(0.0, d - min_clip) for d in durations]
            shrink_total = sum(shrinkable)
            if shrink_total > 0:
                for i in range(len(durations)):
                    cut = excess * (shrinkable[i] / shrink_total)
                    durations[i] = max(min_clip, durations[i] - cut)

        if sum(durations) < target_duration:
            deficit = target_duration - sum(durations)
            headroom = [max(0.0, limit - dur) for limit, dur in zip(max_avail, durations)]
            room_total = sum(headroom)
            if room_total > 0:
                for i in range(len(durations)):
                    add = deficit * (headroom[i] / room_total)
                    durations[i] = min(max_avail[i], durations[i] + add)

        items: List[TimelineItem] = []
        for idx, match in enumerate(matches):
            clip_duration = max(min_clip, durations[idx])
            scene_start = match.scene.start
            scene_end = match.scene.end
            scene_mid = (scene_start + scene_end) / 2.0
            start = max(0.0, scene_mid - (clip_duration / 2.0))
            end = start + clip_duration
            if end > scene_end + 1.0:
                end = scene_end + 1.0
                start = max(0.0, end - clip_duration)

            items.append(
                TimelineItem(
                    beat_type=match.beat.beat_type,
                    source_start=scene_start,
                    source_end=scene_end,
                    clip_start=round(start, 3),
                    clip_end=round(end, 3),
                    narration_text=match.beat.text,
                )
            )

        items.sort(key=lambda x: x.clip_start)
        return items
