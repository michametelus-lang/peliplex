"""Generate short-form voice-over script beats from story structure."""
from __future__ import annotations

from typing import Dict, List

from models import PipelineConfig, ScriptBeat, StoryStructure


EMOTIONS: Dict[str, str] = {
    "hook": "intriga",
    "setup": "curiosidad",
    "conflict": "tensión",
    "twist": "sorpresa",
    "climax": "impacto",
    "resolution": "alivio",
}


class ScriptGenerator:
    """Create concise narrative beats aligned to short-video rhythm."""

    def generate(self, story: StoryStructure, config: PipelineConfig) -> List[ScriptBeat]:
        base_map = {
            "hook": story.hook,
            "setup": story.setup,
            "conflict": story.conflict,
            "twist": story.twist,
            "climax": story.climax,
            "resolution": story.resolution,
        }
        weights = {
            "baja": [0.15, 0.17, 0.18, 0.17, 0.2, 0.13],
            "media": [0.14, 0.16, 0.2, 0.16, 0.22, 0.12],
            "alta": [0.12, 0.14, 0.2, 0.16, 0.26, 0.12],
        }[config.intensity]

        beat_types = ["hook", "setup", "conflict", "twist", "climax", "resolution"]
        beats: List[ScriptBeat] = []
        for idx, beat_type in enumerate(beat_types):
            dur = max(
                config.beat_min_duration,
                min(config.beat_max_duration, config.target_total_duration * weights[idx]),
            )
            beats.append(
                ScriptBeat(
                    beat_type=beat_type,
                    text=base_map[beat_type][:180],
                    desired_emotion=EMOTIONS[beat_type],
                    target_duration=round(dur, 2),
                    intensity_weight=1.3 if beat_type == "climax" else 1.0,
                )
            )
        return beats
        
