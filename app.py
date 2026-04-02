"""Streamlit panel for running and inspecting the PeliPlex pipeline."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from config import build_config, ensure_output_dirs
from main import run_pipeline


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _format_mmss(seconds: int) -> str:
    minutes = seconds // 60
    remaining = seconds % 60
    return f"{minutes:02d}:{remaining:02d}"


def _resolve_input_video(manual_path: str, uploaded_file: Any, output_dir: str) -> str:
    """Resolve input path prioritizing uploaded file over manual path."""
    if uploaded_file is not None:
        uploads_dir = Path(output_dir) / "uploads"
        uploads_dir.mkdir(parents=True, exist_ok=True)
        saved_path = uploads_dir / uploaded_file.name
        saved_path.write_bytes(uploaded_file.getbuffer())
        st.sidebar.success(f"Archivo subido y guardado: {saved_path.name}")
        st.sidebar.info(f"Video activo: {saved_path}")
        return str(saved_path)

    if manual_path.strip():
        path = Path(manual_path.strip()).expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"La ruta manual no existe o no es un archivo: {path}")
        st.sidebar.info(f"Video activo: {path}")
        return str(path)

    raise ValueError("Debes subir un video o escribir una ruta manual válida.")


def _build_sidebar() -> dict[str, Any]:
    st.sidebar.header("Configuración")
    st.sidebar.markdown("### Sube un video")
    uploaded_file = st.sidebar.file_uploader(
        "Formatos permitidos",
        type=["mp4", "mkv", "avi", "mov", "webm"],
        accept_multiple_files=False,
    )

    st.sidebar.markdown("### O escribe la ruta del video")
    manual_path = st.sidebar.text_input("Ruta manual", value="")

    mode = st.sidebar.selectbox("Mode", ["auto", "manual"], index=0)
    intensity = st.sidebar.selectbox("Intensity", ["baja", "media", "alta"], index=1)
    duration = st.sidebar.slider("Duración objetivo (s)", min_value=300, max_value=360, value=330)
    st.sidebar.caption(f"Duración elegida: {_format_mmss(duration)} (mm:ss)")
    enable_tts = st.sidebar.checkbox("Enable TTS", value=False)
    enable_monetization = st.sidebar.checkbox("Enable monetization", value=False)
    output_dir = st.sidebar.text_input("Output dir", value="output")

    return {
        "mode": mode,
        "intensity": intensity,
        "target_total_duration": duration,
        "tts_enabled": enable_tts,
        "monetization_enabled": enable_monetization,
        "manual_input_video": manual_path,
        "uploaded_file": uploaded_file,
        "output_dir": output_dir,
        "summary_mode": "viral_story",
        "editor_mode": "narrativo",
        "language": "es",
        "vertical_format": True,
    }


def main() -> None:
    st.set_page_config(page_title="PeliPlex", layout="wide")
    st.title("PeliPlex · Narrativa audiovisual automática")
    st.caption("Sube un video con voz o usa ruta manual para generar una historia resumida de 5–6 minutos.")

    cfg_raw = _build_sidebar()

    if st.button("Ejecutar pipeline", type="primary"):
        try:
            ensure_output_dirs(cfg_raw["output_dir"])
            input_video = _resolve_input_video(
                manual_path=cfg_raw.pop("manual_input_video"),
                uploaded_file=cfg_raw.pop("uploaded_file"),
                output_dir=cfg_raw["output_dir"],
            )
            cfg_raw["input_video"] = input_video
            config = build_config(cfg_raw)
            final_path = run_pipeline(config)
            st.success(f"Pipeline completado. Video final: {final_path}")
            st.session_state["peliplex_output"] = config.output_dir
            st.session_state["peliplex_final"] = str(final_path)
        except Exception as exc:
            st.error(str(exc))

    output_dir = Path(st.session_state.get("peliplex_output", cfg_raw["output_dir"]))
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
