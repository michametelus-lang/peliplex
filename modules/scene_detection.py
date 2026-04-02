"""Scene candidate detection using visual, semantic, and emotional signals."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
from rapidfuzz import fuzz

from models import SceneCandidate, SummaryResult, TranscriptSegment
from utils import normalize_text, save_json


class SceneDetector:
    """Create ranked scene candidates with relevance score."""

    def __init__(self, emotion_keywords_path: Path) -> None:
        with emotion_keywords_path.open("r", encoding="utf-8") as f:
            self.emotion_keywords: Dict[str, List[str]] = json.load(f)

    @staticmethod
    def compute_relevance_score(text_score: float, emotion_score: float, visual_score: float) -> float:
        """Compute mandatory scene relevance score."""
        return (text_score * 0.5) + (emotion_score * 0.3) + (visual_score * 0.2)

    def _emotion_score(self, text: str) -> float:
        t = text.lower()
        hits = sum(t.count(w) for words in self.emotion_keywords.values() for w in words)
        return min(1.0, hits / 6.0)

    def _semantic_score(self, text: str, summary: str) -> float:
        return fuzz.token_set_ratio(normalize_text(text), normalize_text(summary)) / 100.0

    def _visual_scores(self, video_path: str, segment_count: int) -> List[float]:
        try:
            import cv2  # type: ignore

            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
            if total_frames <= 1:
                return [0.4] * segment_count
            sample = max(1, total_frames // max(1, segment_count))
            scores: List[float] = []
            prev_gray = None
            for i in range(segment_count):
                cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames - 1, i * sample))
                ok, frame = cap.read()
                if not ok:
                    scores.append(0.4)
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if prev_gray is None:
                    scores.append(0.4)
                else:
                    diff = float(np.mean(cv2.absdiff(gray, prev_gray))) / 255.0
                    scores.append(min(1.0, diff * 2.0))
                prev_gray = gray
            cap.release()
            return scores
        except Exception:
            return [0.45] * segment_count

    def detect(
        self,
        video_path: str,
        transcript: List[TranscriptSegment],
        summary: SummaryResult,
        min_duration: float = 2.0,
        min_gap: float = 1.0,
        min_relevance: float = 0.3,
        save_path: Path | None = None,
    ) -> List[SceneCandidate]:
        """Detect candidate scenes aligned with summary and emotional peaks."""
        visual_scores = self._visual_scores(video_path, len(transcript))
        candidates: List[SceneCandidate] = []

        for idx, seg in enumerate(transcript):
            duration = seg.end - seg.start
            if duration < min_duration:
                continue
            semantic_score = self._semantic_score(seg.text, summary.summary_text)
            emotion_score = self._emotion_score(seg.text)
            visual_score = visual_scores[idx] if idx < len(visual_scores) else 0.4
            relevance = self.compute_relevance_score(semantic_score, emotion_score, visual_score)
            if relevance < min_relevance:
                continue
            candidates.append(
                SceneCandidate(
                    start=seg.start,
                    end=seg.end,
                    transcript_text=seg.text,
                    emotion_score=round(emotion_score, 4),
                    visual_score=round(visual_score, 4),
                    semantic_score=round(semantic_score, 4),
                    relevance_score=round(relevance, 4),
                )
            )

        # Remove near-duplicates / very close scenes.
        filtered: List[SceneCandidate] = []
        for c in sorted(candidates, key=lambda x: x.start):
            if filtered and c.start - filtered[-1].start < min_gap:
                if c.relevance_score > filtered[-1].relevance_score:
                    filtered[-1] = c
                continue
            filtered.append(c)

        if save_path:
            save_json(save_path, [c.model_dump() for c in filtered])
        return filtered
