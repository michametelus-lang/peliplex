"""Central configuration for PeliPlex."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from exceptions import InvalidConfigurationError
from models import PipelineConfig


DEFAULT_DIRS = [
    "transcripts",
    "summaries",
    "scripts",
    "scenes",
    "clips",
    "edits",
    "metadata",
    "uploads",
]


def build_config(raw: Dict[str, Any]) -> PipelineConfig:
    """Create validated PipelineConfig from raw arguments."""
    try:
        cfg = PipelineConfig(**raw)
        cfg.validate()
        return cfg
    except Exception as exc:
        raise InvalidConfigurationError(str(exc)) from exc


def ensure_output_dirs(base: str) -> None:
    """Create all output directories expected by the pipeline."""
    base_path = Path(base)
    base_path.mkdir(parents=True, exist_ok=True)
    for d in DEFAULT_DIRS:
        (base_path / d).mkdir(parents=True, exist_ok=True)
