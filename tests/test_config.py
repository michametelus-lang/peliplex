import pytest

from config import build_config
from exceptions import InvalidConfigurationError


def test_valid_config():
    cfg = build_config(
        {
            "input_video": "demo.mp4",
            "target_total_duration": 45,
            "beat_min_duration": 2.0,
            "beat_max_duration": 8.0,
        }
    )
    assert cfg.mode == "auto"


def test_invalid_duration_raises():
    with pytest.raises(InvalidConfigurationError):
        build_config({"input_video": "demo.mp4", "target_total_duration": 10})
