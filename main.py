"""PeliPlex main orchestrator and CLI."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List

from config import build_config, ensure_output_dirs
from models import PipelineConfig, ScriptBeat, TranscriptSegment
from modules.clip_generator import ClipGenerator
from modules.editor import Editor
from modules.monetization import MonetizationHelper
from modules.scene_detection import SceneDetector
from modules.scene_matcher import SceneMatcher
from modules.script_generator import ScriptGenerator
from modules.story_analyzer import StoryAnalyzer
from modules.style_detector import StyleDetector
from modules.summarization import Summarizer
from modules.timeline_planner import TimelinePlanner
from modules.transcription import TranscriptionService
from modules.tts import TTSGenerator
from utils import check_ffmpeg_installed, save_json, setup_logging

logger = logging.getLogger(__name__)


def _auto_tune(config: PipelineConfig, transcript: List[TranscriptSegment]) -> PipelineConfig:
    if config.mode != "auto":
        return config

    style = StyleDetector().predict(transcript)
    raw = config.model_dump()
    raw["style"] = style.primary_style

    token_count = sum(len(seg.text.split()) for seg in transcript)
    if token_count > 3000:
        raw["intensity"] = "alta"
        raw["target_total_duration"] = min(360, max(330, config.target_total_duration))
    elif token_count < 350:
        raw["intensity"] = "baja"
        raw["target_total_duration"] = max(300, min(330, config.target_total_duration))
    else:
        raw["intensity"] = "media"

    tuned = build_config(raw)
    logger.info(
        "AUTO mode ajustó style=%s intensity=%s duration=%ss",
        tuned.style,
        tuned.intensity,
        tuned.target_total_duration,
    )
    return tuned


def run_pipeline(config: PipelineConfig) -> Path:
    """Run the full narrative-first short video generation pipeline."""
    setup_logging()
    check_ffmpeg_installed()
    ensure_output_dirs(config.output_dir)
    out = Path(config.output_dir)

    transcript = TranscriptionService().transcribe(
        config.input_video,
        language=config.language,
        save_path=out / "transcripts" / "transcript.json",
    )

    config = _auto_tune(config, transcript)

    summary = Summarizer().summarize(transcript, mode=config.summary_mode)
    save_json(out / "summaries" / "summary.json", summary.model_dump())

    story = StoryAnalyzer().analyze(transcript, summary)
    save_json(out / "metadata" / "story_structure.json", story.model_dump())

    beats: List[ScriptBeat] = ScriptGenerator().generate(story, config)
    save_json(out / "scripts" / "script_beats.json", [b.model_dump() for b in beats])

    scenes = SceneDetector(Path("prompts") / "emotion_keywords.json").detect(
        video_path=config.input_video,
        transcript=transcript,
        summary=summary,
        save_path=out / "scenes" / "scene_candidates.json",
    )

    matches = SceneMatcher().match(
        beats,
        scenes,
        target_duration=config.target_total_duration,
        intensity=config.intensity,
    )
    save_json(out / "metadata" / "scene_matches.json", [m.model_dump() for m in matches])

    timeline = TimelinePlanner().plan(
        matches,
        intensity=config.intensity,
        target_duration=config.target_total_duration,
    )
    save_json(out / "metadata" / "timeline_plan.json", [t.model_dump() for t in timeline])

    clip_paths = ClipGenerator().export(
        config.input_video,
        timeline,
        out / "clips",
        intensity=config.intensity,
        target_duration=config.target_total_duration,
    )

    tts_audio = None
    if config.tts_enabled:
        tts_audio = TTSGenerator().generate(beats, out / "edits" / "narration.wav")

    title = story.hook[:70] if config.include_title_card else None
    final_path = Editor().assemble(
        clip_paths=clip_paths,
        output_path=out / "edits" / "final_video.mp4",
        target_duration=config.target_total_duration,
        editor_mode=config.editor_mode,
        title=title,
        tts_audio=tts_audio,
        vertical_format=config.vertical_format,
    )

    if config.monetization_enabled:
        style = StyleDetector().predict(transcript)
        metadata = MonetizationHelper().build_metadata(story, style)
        save_json(out / "metadata" / "monetization.json", metadata.model_dump())

    return final_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PeliPlex - generador narrativo de videos cortos")
    parser.add_argument("--input", required=True, help="Ruta del video de entrada")
    parser.add_argument("--mode", default="auto", choices=["auto", "manual"])
    parser.add_argument("--style", default=None, choices=["accion", "drama", "terror", "misterio", "romance"])
    parser.add_argument("--intensity", default="media", choices=["baja", "media", "alta"])
    parser.add_argument("--summary-mode", default="viral_story", choices=["neutral", "viral_story"])
    parser.add_argument("--editor-mode", default="narrativo", choices=["narrativo", "lista_escenas", "highlights"])
    parser.add_argument("--enable-tts", action="store_true")
    parser.add_argument("--enable-monetization", action="store_true")
    parser.add_argument("--target-duration", type=int, default=330, help="Duración objetivo en segundos (300-360)")
    parser.add_argument("--language", default="es")
    parser.add_argument("--vertical-format", action="store_true")
    parser.add_argument("--output-dir", default="output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = build_config(
        {
            "mode": args.mode,
            "style": args.style,
            "intensity": args.intensity,
            "summary_mode": args.summary_mode,
            "editor_mode": args.editor_mode,
            "tts_enabled": args.enable_tts,
            "monetization_enabled": args.enable_monetization,
            "input_video": args.input,
            "output_dir": args.output_dir,
            "language": args.language,
            "target_total_duration": args.target_duration,
            "vertical_format": args.vertical_format,
        }
    )
    result = run_pipeline(config)
    logger.info("Video final exportado en: %s", result)


if __name__ == "__main__":
    main()
