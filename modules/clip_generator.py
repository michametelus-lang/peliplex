"""Generate physical clips from timeline with duration-aware cutting."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from moviepy import VideoFileClip

from exceptions import ClipExportError
from models import TimelineItem

logger = logging.getLogger(__name__)


class ClipGenerator:
    """Cut source video into clip files according to timeline items."""

    def _bounds_by_intensity(self, intensity: str) -> tuple[float, float]:
        return {
            "alta": (2.0, 5.0),
            "media": (2.5, 8.0),
            "baja": (3.0, 12.0),
        }[intensity]

    def export(
        self,
        video_path: str,
        timeline: List[TimelineItem],
        clips_dir: Path,
        intensity: str,
        target_duration: int,
    ) -> List[Path]:
        """Export clips while preserving pacing and not exceeding total duration target."""
        clips_dir.mkdir(parents=True, exist_ok=True)
        output_paths: List[Path] = []
        min_dur, max_dur = self._bounds_by_intensity(intensity)

        try:
            with VideoFileClip(video_path) as source:
                consumed = 0.0
                for idx, item in enumerate(timeline):
                    if consumed >= target_duration:
                        break

                    start = max(0.0, item.clip_start)
                    requested = max(min_dur, item.clip_end - item.clip_start)
                    requested = min(max_dur, requested)

                    remaining = max(0.0, target_duration - consumed)
                    duration = min(requested, remaining)
                    if duration < 2.0:
                        break

                    end = min(source.duration, start + duration)
                    if end - start < 2.0:
                        continue

                    sub = source.subclipped(start, end)
                    out = clips_dir / f"clip_{idx:03d}_{item.beat_type}.mp4"
                    sub.write_videofile(
                        str(out),
                        audio_codec="aac",
                        codec="libx264",
                        preset="ultrafast",
                        threads=2,
                        logger=None,
                    )
                    sub.close()
                    consumed += end - start
                    output_paths.append(out)

            return output_paths
        except Exception as exc:
            logger.exception("Error exportando clips")
            raise ClipExportError(str(exc)) from exc
