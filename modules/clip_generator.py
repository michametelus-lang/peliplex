"""Generate physical clips from timeline."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from moviepy.video.io.VideoFileClip import VideoFileClip

from exceptions import ClipExportError
from models import TimelineItem

logger = logging.getLogger(__name__)


class ClipGenerator:
    """Cut source video into clip files according to timeline items."""

    def export(self, video_path: str, timeline: List[TimelineItem], clips_dir: Path) -> List[Path]:
        clips_dir.mkdir(parents=True, exist_ok=True)
        output_paths: List[Path] = []
        try:
            with VideoFileClip(video_path) as source:
                for idx, item in enumerate(timeline):
                    start = max(0.0, item.clip_start)
                    end = min(source.duration, max(start + 2.0, item.clip_end))
                    sub = source.subclipped(start, end)
                    out = clips_dir / f"clip_{idx:02d}_{item.beat_type}.mp4"
                    sub.write_videofile(str(out), audio_codec="aac", logger=None)
                    output_paths.append(out)
            return output_paths
        except Exception as exc:
            logger.exception("Error exportando clips")
            raise ClipExportError(str(exc)) from exc
