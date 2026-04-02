from models import SceneCandidate, ScriptBeat
from modules.scene_matcher import SceneMatcher


def test_scene_selection_per_beat():
    beats = [
        ScriptBeat(beat_type="hook", text="secreto inesperado", desired_emotion="intriga", target_duration=4),
        ScriptBeat(beat_type="climax", text="giro brutal", desired_emotion="impacto", target_duration=6),
    ]
    scenes = [
        SceneCandidate(start=1, end=5, transcript_text="descubren un secreto inesperado", emotion_score=0.8, visual_score=0.6, semantic_score=0.9, relevance_score=0.8),
        SceneCandidate(start=6, end=12, transcript_text="todo cambia con un giro brutal", emotion_score=0.9, visual_score=0.9, semantic_score=0.95, relevance_score=0.93),
    ]
    matches = SceneMatcher().match(beats, scenes)
    assert len(matches) == 2
    assert matches[0].scene.start <= matches[1].scene.start
