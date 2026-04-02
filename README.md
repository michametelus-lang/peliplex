# PeliPlex

PeliPlex transforma videos largos en una **historia narrada de 5–6 minutos** (300–360s), priorizando estabilidad del pipeline y coherencia básica entre narración y escena.

## Flujo estable (MVP)
1. Entrada de video (subida en Streamlit o ruta manual).
2. Transcripción local con Whisper (CPU).
3. Resumen narrativo corto y estable.
4. Estructura de historia + beats.
5. Detección de escenas candidatas.
6. Matching beat → escena.
7. Plan de timeline con control de duración objetivo.
8. Exportación de clips.
9. Ensamblado final y visualización en panel.

## Requisitos
- Python 3.11
- FFmpeg en `PATH`
- CPU (no GPU obligatoria)

## Instalación
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar panel
```bash
streamlit run app.py
```

En el panel:
- **Sube un video** (`mp4`, `mkv`, `avi`, `mov`, `webm`) o usa **ruta manual**.
- Si subes archivo, se guarda en `output/uploads/` y tiene prioridad.
- Selecciona duración objetivo entre **300 y 360 segundos** (default **330**).
- Ejecuta y revisa tabs: Transcripción, Resumen, Narrativa, Escenas, Matching, Clips y Final.

## Ejecutar por CLI
```bash
python main.py --input path\\video.mp4 --target-duration 330 --mode manual
```

## Qué esperar
- `output/transcripts/transcript.json`
- `output/summaries/summary.json`
- `output/metadata/story_structure.json`
- `output/scripts/script_beats.json`
- `output/scenes/scene_candidates.json`
- `output/metadata/scene_matches.json`
- `output/metadata/timeline_plan.json`
- `output/clips/*.mp4`
- `output/edits/final_video.mp4`

## Nota de estabilidad
Este MVP prioriza robustez end-to-end sobre sofisticación: reglas simples, errores claros y compatibilidad consistente con MoviePy 2.x.
