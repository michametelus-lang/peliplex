"""Streamlit panel for running and inspecting the PeliPlex pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from config import build_config
from main import run_pipeline


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _build_sidebar() -> dict[str, Any]:
    st.sidebar.header("Configuración")
    input_video = st.sidebar.text_input("Input video", value="")
    mode = st.sidebar.selectbox("Mode", ["auto", "manual"], index=0)
    intensity = st.sidebar.selectbox("Intensity", ["baja", "media", "alta"], index=1)
    duration = st.sidebar.slider("Duración objetivo (s)", min_value=20, max_value=90, value=45)
    enable_tts = st.sidebar.checkbox("Enable TTS", value=False)
    enable_monetization = st.sidebar.checkbox("Enable monetization", value=False)

    return {
        "mode": mode,
        "intensity": intensity,
        "target_total_duration": duration,
        "tts_enabled": enable_tts,
        "monetization_enabled": enable_monetization,
        "input_video": input_video,
        "output_dir": "output",
        "summary_mode": "viral_story",
        "editor_mode": "narrativo",
        "language": "es",
        "vertical_format": True,
    }


def main() -> None:
    st.set_page_config(page_title="PeliPlex", layout="wide")
    st.title("PeliPlex · Narrativa audiovisual automática")
    st.caption("Convierte videos largos en historias cortas narradas para Shorts/Reels/TikTok.")

    cfg_raw = _build_sidebar()

    if st.button("Ejecutar pipeline", type="primary"):
        if not cfg_raw["input_video"]:
            st.error("Debes indicar la ruta del video de entrada.")
        else:
            try:
                config = build_config(cfg_raw)
                final_path = run_pipeline(config)
                st.success(f"Pipeline completado. Video final: {final_path}")
                st.session_state["peliplex_output"] = config.output_dir
                st.session_state["peliplex_final"] = str(final_path)
            except Exception as exc:  # runtime pipeline errors should be shown in UI
                st.exception(exc)

    output_dir = Path(st.session_state.get("peliplex_output", "output"))

    tabs = st.tabs(["Transcripción", "Resumen", "Narrativa", "Escenas", "Matching", "Clips", "Final"])

    with tabs[0]:
        st.subheader("Transcripción")
        st.json(_read_json(output_dir / "transcripts" / "transcript.json") or {})

    with tabs[1]:
        st.subheader("Resumen")
        st.json(_read_json(output_dir / "summaries" / "summary.json") or {})

    with tabs[2]:
        st.subheader("Estructura y guion narrativo")
        st.markdown("**Story structure**")
        st.json(_read_json(output_dir / "metadata" / "story_structure.json") or {})
        st.markdown("**Script beats**")
        st.json(_read_json(output_dir / "scripts" / "script_beats.json") or [])

    with tabs[3]:
        st.subheader("Escenas candidatas")
        st.json(_read_json(output_dir / "scenes" / "scene_candidates.json") or [])

    with tabs[4]:
        st.subheader("Matching beat → escena")
        st.json(_read_json(output_dir / "metadata" / "scene_matches.json") or [])

    with tabs[5]:
        st.subheader("Clips exportados")
        clip_dir = output_dir / "clips"
        clips = sorted(str(p) for p in clip_dir.glob("*.mp4")) if clip_dir.exists() else []
        st.write(clips or "Sin clips aún")

    with tabs[6]:
        st.subheader("Resultado final")
        final_video = Path(st.session_state.get("peliplex_final", output_dir / "edits" / "final_video.mp4"))
        if final_video.exists():
            st.video(str(final_video))
        else:
            st.info("Ejecuta el pipeline para generar el video final.")


if __name__ == "__main__":
    main()
