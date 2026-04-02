"""Text-to-speech generation with edge-tts primary and pyttsx3 fallback."""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List

from exceptions import TTSError
from models import ScriptBeat


class TTSGenerator:
    """Generate narration audio from script beats."""

    async def _edge_tts(self, text: str, output_path: Path, voice: str = "es-ES-AlvaroNeural") -> None:
        import edge_tts  # type: ignore

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))

    def _pyttsx3(self, text: str, output_path: Path) -> None:
        import pyttsx3  # type: ignore

        engine = pyttsx3.init()
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()

    def generate(self, beats: List[ScriptBeat], output_path: Path, preferred: str = "edge") -> Path:
        """Create a single narration track from all beats."""
        text = " ".join(b.text for b in beats)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if preferred == "edge":
            try:
                asyncio.run(self._edge_tts(text, output_path))
                return output_path
            except Exception:
                pass

        try:
            self._pyttsx3(text, output_path)
            return output_path
        except Exception as exc:
            raise TTSError(f"No se pudo generar TTS: {exc}") from exc
