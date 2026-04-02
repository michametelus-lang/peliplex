"""Generate publication metadata for short-form platforms."""
from __future__ import annotations

from models import MonetizationResult, StoryStructure, StylePrediction


class MonetizationHelper:
    """Create generic, non-misleading metadata."""

    def build_metadata(self, story: StoryStructure, style: StylePrediction) -> MonetizationResult:
        title = f"Historia corta de {style.primary_style}: {story.hook[:50]}"
        description = (
            "Resumen narrativo automático generado desde contenido propio. "
            "Incluye hook, conflicto, clímax y cierre en formato corto."
        )
        hashtags = ["#shorts", "#reels", "#tiktok", f"#{style.primary_style}", "#historiacorta"]
        return MonetizationResult(title=title, description=description, hashtags=hashtags)
