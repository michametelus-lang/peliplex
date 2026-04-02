"""Narrative beat to scene matching with coherence-first scoring."""
from __future__ import annotations

from typing import List

from rapidfuzz import fuzz

from models import SceneCandidate, SceneMatch, ScriptBeat
from utils import normalize_text


class SceneMatcher:
    """Assign best scene candidate to each narrative beat."""

    @staticmethod
    def compute_narrative_match_score(
        semantic_match: float,
        emotion_match: float,
        visual_fit: float,
        timeline_fit: float,
        diversity_bonus: float,
    ) -> float:
        """Compute mandatory narrative match score."""
        return (
            (semantic_match * 0.35)
            + (emotion_match * 0.25)
            + (visual_fit * 0.15)
            + (timeline_fit * 0.15)
            + (diversity_bonus * 0.10)
        )

    def _timeline_fit(self, scene_start: float, prev_scene_start: float | None) -> float:
        if prev_scene_start is None:
            return 1.0
        gap = scene_start - prev_scene_start
        if gap >= 0:
            return min(1.0, 0.6 + (gap / 25.0))
        return 0.2

    def _emotion_match(self, beat_emotion: str, text: str) -> float:
        return fuzz.partial_ratio(beat_emotion.lower(), text.lower()) / 100.0

    def _expand_beats(self, beats: List[ScriptBeat], target_duration: int, intensity: str) -> List[ScriptBeat]:
        avg_clip = {"alta": 4.0, "media": 6.0, "baja": 8.0}[intensity]
        desired_count = max(len(beats), int(round(target_duration / avg_clip)))
        if desired_count <= len(beats):
            return beats

        by_type = {beat.beat_type: beat for beat in beats}
        expanded: List[ScriptBeat] = []
        for idx in range(desired_count):
            progress = idx / max(1, desired_count - 1)
            if progress < 0.12:
                beat_type = "hook"
            elif progress < 0.28:
                beat_type = "setup"
            elif progress < 0.58:
                beat_type = "conflict"
            elif progress < 0.76:
                beat_type = "twist"
            elif progress < 0.92:
                beat_type = "climax"
            else:
                beat_type = "resolution"
            expanded.append(by_type.get(beat_type, beats[min(idx, len(beats) - 1)]))
        return expanded

    def match(
        self,
        beats: List[ScriptBeat],
        scenes: List[SceneCandidate],
        target_duration: int = 45,
        intensity: str = "media",
    ) -> List[SceneMatch]:
        """Return selected scenes maximizing narrative coherence and target pacing."""
        if not scenes or not beats:
            return []

        planned_beats = self._expand_beats(beats, target_duration=target_duration, intensity=intensity)
        max_scenes = min(len(scenes), len(planned_beats))

        matches: List[SceneMatch] = []
        usage_count = {idx: 0 for idx in range(len(scenes))}
        prev_start = None

        for beat in planned_beats:
            ranked = []
            for idx, scene in enumerate(scenes):
                semantic = fuzz.token_set_ratio(normalize_text(beat.text), normalize_text(scene.transcript_text)) / 100.0
                emotion = self._emotion_match(beat.desired_emotion, scene.transcript_text)
                visual = scene.visual_score
                timeline = self._timeline_fit(scene.start, prev_start)
                diversity = max(0.0, 1.0 - (usage_count[idx] * 0.35))

                if beat.beat_type in {"hook", "climax"}:
                    visual = min(1.0, visual * 1.2)

                score = self.compute_narrative_match_score(semantic, emotion, visual, timeline, diversity)
                ranked.append((score, idx, semantic, emotion, visual, timeline, diversity))

            ranked.sort(key=lambda x: x[0], reverse=True)
            best = ranked[0]
            _, idx, semantic, emotion, visual, timeline, diversity = best
            usage_count[idx] += 1
            selected = scenes[idx]
            prev_start = selected.start
            matches.append(
                SceneMatch(
                    beat=beat,
                    scene=selected,
                    semantic_match=round(semantic, 4),
                    emotion_match=round(emotion, 4),
                    visual_fit=round(visual, 4),
                    timeline_fit=round(timeline, 4),
                    diversity_bonus=round(diversity, 4),
                    narrative_match_score=round(best[0], 4),
                )
            )
            if len(matches) >= max_scenes:
                break

        return matches
