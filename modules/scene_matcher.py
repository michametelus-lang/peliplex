"""Narrative beat to scene matching with coherence-first scoring."""
from __future__ import annotations

from typing import List, Set

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
        return 1.0 if scene_start >= prev_scene_start else 0.2

    def _emotion_match(self, beat_emotion: str, text: str) -> float:
        return fuzz.partial_ratio(beat_emotion.lower(), text.lower()) / 100.0

    def match(self, beats: List[ScriptBeat], scenes: List[SceneCandidate]) -> List[SceneMatch]:
        """Return selected scene per beat, maximizing coherence and progression."""
        if not scenes:
            return []

        matches: List[SceneMatch] = []
        used_indices: Set[int] = set()
        prev_start = None

        for beat in beats:
            ranked = []
            for idx, scene in enumerate(scenes):
                semantic = fuzz.token_set_ratio(normalize_text(beat.text), normalize_text(scene.transcript_text)) / 100.0
                emotion = self._emotion_match(beat.desired_emotion, scene.transcript_text)
                visual = scene.visual_score
                timeline = self._timeline_fit(scene.start, prev_start)
                diversity = 0.0 if idx in used_indices else 1.0

                # hook/climax priority: require visually stronger options
                if beat.beat_type in {"hook", "climax"}:
                    visual = min(1.0, visual * 1.2)

                score = self.compute_narrative_match_score(semantic, emotion, visual, timeline, diversity)
                ranked.append((score, idx, semantic, emotion, visual, timeline, diversity))

            ranked.sort(key=lambda x: x[0], reverse=True)
            best = ranked[0]
            _, idx, semantic, emotion, visual, timeline, diversity = best
            used_indices.add(idx)
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

        return matches
