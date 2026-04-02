"""Final video assembly module."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from moviepy.editor import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip, concatenate_videoclips


class Editor:
    """Assemble final video using selected mode (narrativo prioritized)."""

    def assemble(
        self,
        clip_paths: List[Path],
        output_path: Path,
        editor_mode: str = "narrativo",
        title: Optional[str] = None,
        tts_audio: Optional[Path] = None,
        vertical_format: bool = True,
    ) -> Path:
        clips = [VideoFileClip(str(p)) for p in clip_paths]
        try:
            final = concatenate_videoclips(clips, method="compose")

            if vertical_format:
                final = final.resize(height=1920)

            if title and editor_mode == "narrativo":
                text = TextClip(txt=title, fontsize=64, color="white").set_duration(2.0).set_position(("center", "top"))
                final = CompositeVideoClip([final, text])

            if tts_audio and Path(tts_audio).exists():
                narration = AudioFileClip(str(tts_audio))
                final = final.set_audio(narration)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            final.write_videofile(str(output_path), codec="libx264", audio_codec="aac", logger=None)
            return output_path
        finally:
            for c in clips:
                c.close()
