from modules.scene_detection import SceneDetector
from modules.scene_matcher import SceneMatcher


def test_relevance_formula():
    score = SceneDetector.compute_relevance_score(0.8, 0.5, 0.4)
    assert round(score, 4) == round((0.8 * 0.5) + (0.5 * 0.3) + (0.4 * 0.2), 4)


def test_narrative_formula():
    score = SceneMatcher.compute_narrative_match_score(0.7, 0.6, 0.8, 0.9, 1.0)
    expected = (0.7 * 0.35) + (0.6 * 0.25) + (0.8 * 0.15) + (0.9 * 0.15) + (1.0 * 0.10)
    assert round(score, 4) == round(expected, 4)
    
