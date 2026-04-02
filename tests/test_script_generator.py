from models import PipelineConfig, StoryStructure
from modules.script_generator import ScriptGenerator


def test_generates_six_beats():
    story = StoryStructure(
        hook="algo extraño arranca",
        setup="presentación de contexto",
        conflict="aparece un problema",
        twist="nadie lo esperaba",
        climax="momento máximo",
        resolution="final breve",
    )
    cfg = PipelineConfig(input_video="demo.mp4", target_total_duration=330)
    beats = ScriptGenerator().generate(story, cfg)
    assert len(beats) == 6
    assert beats[0].beat_type == "hook"
