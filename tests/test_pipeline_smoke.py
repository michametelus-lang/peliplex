from pathlib import Path

from config import build_config
from models import SummaryResult, TranscriptSegment
from modules.scene_detection import SceneDetector
from modules.scene_matcher import SceneMatcher
from modules.script_generator import ScriptGenerator
from modules.story_analyzer import StoryAnalyzer
from modules.timeline_planner import TimelinePlanner


def test_pipeline_logic_smoke():
    transcript = [
        TranscriptSegment(start=0, end=3, text="inicio con tensión y secreto"),
        TranscriptSegment(start=3, end=7, text="la situación empeora y crece el riesgo"),
        TranscriptSegment(start=7, end=12, text="gran giro con cierre final"),
    ]
    summary = SummaryResult(mode="viral_story", summary_text="historia con secreto, riesgo y giro", key_points=["secreto", "riesgo", "giro"], highlights=["giro final"])

    story = StoryAnalyzer().analyze(transcript, summary)
    cfg = build_config({"input_video": "demo.mp4", "target_total_duration": 35})
    beats = ScriptGenerator().generate(story, cfg)
    detector = SceneDetector(Path("prompts") / "emotion_keywords.json")
    scenes = detector.detect("fake.mp4", transcript, summary)
    matches = SceneMatcher().match(beats, scenes)
    timeline = TimelinePlanner().plan(matches, cfg.intensity)

    assert len(beats) == 6
    assert len(scenes) >= 1
    assert len(matches) >= 1
    assert len(timeline) >= 1
