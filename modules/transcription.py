"""Video transcription module using Whisper with CPU-safe settings."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from moviepy import VideoFileClip

from exceptions import EmptyTranscriptionError, ModelLoadingError, VideoFileNotFoundError, VideoHasNoAudioError
from models import TranscriptSegment
from utils import save_json

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Transcribe video audio into timestamped text segments."""

    def __init__(self, model_name: str = "base") -> None:
        self.model_name = model_name

    def _load_model(self):
        try:
            import whisper  # type: ignore

            return whisper.load_model(self.model_name, device="cpu")
        except Exception as exc:
            raise ModelLoadingError(f"No se pudo cargar Whisper en CPU: {exc}") from exc

    def validate_video(self, video_path: str) -> None:
        path = Path(video_path)
        if not path.exists() or not path.is_file():
            raise VideoFileNotFoundError(f"No existe el archivo: {video_path}")

        with VideoFileClip(video_path) as clip:
            if clip.audio is None:
                raise VideoHasNoAudioError("El video no tiene pista de audio para transcribir")

    def transcribe(self, video_path: str, language: str = "es", save_path: Optional[Path] = None) -> List[TranscriptSegment]:
        """Transcribe a video and return timestamped segments."""
        self.validate_video(video_path)
        model = self._load_model()

        try:
            result = model.transcribe(
                video_path,
                language=language,
                verbose=False,
                fp16=False,
                temperature=0.0,
                condition_on_previous_text=True,
            )
        except Exception as exc:
            raise EmptyTranscriptionError(f"Fallo durante transcripción Whisper: {exc}") from exc

        segments = [
            TranscriptSegment(start=float(seg["start"]), end=float(seg["end"]), text=str(seg["text"]).strip())
            for seg in result.get("segments", [])
            if str(seg.get("text", "")).strip()
        ]

        if not segments:
            raise EmptyTranscriptionError("Whisper devolvió transcripción vacía. Verifica audio/idioma del video.")

        if save_path:
            save_json(save_path, [s.model_dump() for s in segments])
        logger.info("Transcripción completada con %s segmentos", len(segments))
        return segments
