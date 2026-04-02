"""Shared data models for the PeliPlex pipeline."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Literal


@dataclass
class ModelMixin:
    def model_dump(self):
        return asdict(self)


@dataclass
class TranscriptSegment(ModelMixin):
    start: float
    end: float
    text: str


@dataclass
class SummaryResult(ModelMixin):
    mode: Literal["neutral", "viral_story"]
    summary_text: str
    key_points: List[str] = field(default_factory=list)
    highlights: List[str] = field(default_factory=list)


@dataclass
class StoryStructure(ModelMixin):
    hook: str
    setup: str
    conflict: str
    twist: str
    climax: str
    resolution: str


@dataclass
class ScriptBeat(ModelMixin):
    beat_type: Literal["hook", "setup", "conflict", "twist", "climax", "resolution"]
    text: str
    desired_emotion: str
    target_duration: float
    intensity_weight: float = 1.0


@dataclass
class StylePrediction(ModelMixin):
    primary_style: Literal["accion", "drama", "terror", "misterio", "romance"]
    scores: Dict[str, float]


@dataclass
class SceneCandidate(ModelMixin):
    start: float
    end: float
    transcript_text: str
    emotion_score: float
    visual_score: float
    semantic_score: float
    relevance_score: float


@dataclass
class SceneMatch(ModelMixin):
    beat: ScriptBeat
    scene: SceneCandidate
    semantic_match: float
    emotion_match: float
    visual_fit: float
    timeline_fit: float
    diversity_bonus: float
    narrative_match_score: float


@dataclass
class TimelineItem(ModelMixin):
    beat_type: str
    source_start: float
    source_end: float
    clip_start: float
    clip_end: float
    narration_text: str


@dataclass
class ClipPlan(ModelMixin):
    items: List[TimelineItem]


@dataclass
class MonetizationResult(ModelMixin):
    title: str
    description: str
    hashtags: List[str]


@dataclass
class PipelineConfig(ModelMixin):
    mode: Literal["auto", "manual"] = "auto"
    style: Literal["accion", "drama", "terror", "misterio", "romance"] | None = None
    intensity: Literal["baja", "media", "alta"] = "media"
    summary_mode: Literal["neutral", "viral_story"] = "viral_story"
    editor_mode: Literal["narrativo", "lista_escenas", "highlights"] = "narrativo"
    tts_enabled: bool = False
    monetization_enabled: bool = False
    input_video: str = ""
    output_dir: str = "output"
    language: str = "es"
    target_total_duration: int = 45
    beat_min_duration: float = 2.0
    beat_max_duration: float = 9.0
    vertical_format: bool = True
    include_title_card: bool = True

    def validate(self) -> None:
        if not self.input_video:
            raise ValueError("input_video es obligatorio")
        if not 20 <= self.target_total_duration <= 90:
            raise ValueError("target_total_duration debe estar entre 20 y 90 segundos")
        if self.beat_min_duration < 1.5:
            raise ValueError("beat_min_duration debe ser >= 1.5")
        if self.beat_max_duration < self.beat_min_duration:
            raise ValueError("beat_max_duration debe ser >= beat_min_duration")
