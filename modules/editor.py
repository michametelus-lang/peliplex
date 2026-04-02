"""Final video assembly module with strict total-duration control."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip, concatenate_videoclips

from exceptions import VideoAssemblyError


class Editor:
    """Assemble final video using selected mode (narrativo prioritized)."""

    def assemble(
        self,
        clip_paths: List[Path],
        output_path: Path,
        target_duration: int,
        editor_mode: str = "narrativo",
        title: Optional[str] = None,
        tts_audio: Optional[Path] = None,
        vertical_format: bool = True,
    ) -> Path:
        if not clip_paths:
            raise VideoAssemblyError("No hay clips para ensamblar")

        clips = [VideoFileClip(str(p)) for p in clip_paths]
        narration_clip: Optional[AudioFileClip] = None
        final = None
        try:
            final = concatenate_videoclips(clips, method="compose")
            if final.duration > target_duration:
                final = final.subclipped(0, target_duration)

            if vertical_format:
                final = final.resized(height=1920)

            if title and editor_mode == "narrativo":
                try:
                    text = (
                        TextClip(text=title, font_size=58, color="white")
                        .with_duration(min(2.5, final.duration))
                        .with_position(("center", "top"))
                    )
                    final = CompositeVideoClip([final, text])
                except Exception:
                    pass

            if tts_audio and Path(tts_audio).exists():
                narration_clip = AudioFileClip(str(tts_audio))
                if narration_clip.duration >= final.duration:
                    narration_clip = narration_clip.subclipped(0, final.duration)
                final = final.with_audio(narration_clip)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            final.write_videofile(
                str(output_path),
                codec="libx264",
                audio_codec="aac",
                fps=24,
                preset="ultrafast",
                threads=2,
                logger=None,
            )
            return output_path
        except Exception as exc:
            raise VideoAssemblyError(str(exc)) from exc
        finally:
            if narration_clip is not None:
                narration_clip.close()
            if final is not None:
                final.close()
            for c in clips:
                c.close()
