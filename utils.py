"""Utility helpers for serialization, logging, and external tools."""
from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

from exceptions import FFmpegNotInstalledError


def setup_logging(level: int = logging.INFO) -> None:
    """Configure default logging format for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def save_json(path: Path, payload: Any) -> None:
    """Save JSON payload to disk creating parents if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def check_ffmpeg_installed() -> None:
    """Raise FFmpegNotInstalledError if ffmpeg is not in PATH."""
    if shutil.which("ffmpeg") is None:
        raise FFmpegNotInstalledError("ffmpeg no encontrado en PATH.")


def normalize_text(value: str) -> str:
    """Normalize text for lightweight semantic matching."""
    return " ".join(value.lower().strip().split())
