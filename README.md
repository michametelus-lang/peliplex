PeliPlex

PeliPlex es un sistema modular en Python para transformar videos largos en **historias cortas narradas** (20–90s) para TikTok, Reels y YouTube Shorts.

## Objetivo real
PeliPlex no es un simple resumidor: prioriza la **coherencia entre narración, escena visual y ritmo** para que el resultado se sienta como una historia condensada.

## Pipeline narrativo
1. Transcripción con timestamps (Whisper).
2. Resumen estructurado (neutral o viral_story).
3. Story analyzer (hook, setup, conflict, twist, climax, resolution).
4. Script generator de beats breves para voz en off.
5. Detección de escenas candidatas (texto + emoción + señal visual).
6. Matching beat → escena con scoring narrativo.
7. Plan de timeline.
8. Generación de clips.
9. TTS opcional.
10. Edición final y metadata de publicación.

## Scoring implementado

### Relevance score (scene_detection)
`relevance_score = (texto * 0.5) + (emocion * 0.3) + (visual * 0.2)`

### Narrative match score (scene_matcher)
`narrative_match_score = (semantic_match * 0.35) + (emotion_match * 0.25) + (visual_fit * 0.15) + (timeline_fit * 0.15) + (diversity_bonus * 0.10)`

## Arquitectura

- `main.py`: orquestador del pipeline + CLI.
- `app.py`: panel Streamlit para ejecutar y revisar resultados.
- `config.py`: validación central y creación de carpetas de salida.
- `models.py`: modelos compartidos tipados y serializables para todo el pipeline.
- `exceptions.py`: errores de dominio del pipeline.
- `utils.py`: logging, guardado de JSON y helpers.
- `modules/`: bloques funcionales de narración/transcripción/escenas/edición/TTS.

## Instalación (Windows)
1. Instalar Python 3.10+.
2. Instalar FFmpeg y agregarlo al `PATH`.
3. Crear entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso por CLI

```bash
python main.py \
  --input path\\a\\video.mp4 \
  --mode auto \
  --summary-mode viral_story \
  --editor-mode narrativo \
  --enable-tts \
  --enable-monetization \
  --target-duration 45 \
  --language es \
  --vertical-format
```

### Parámetros CLI
- `--input`
- `--mode {auto,manual}`
- `--style {accion,drama,terror,misterio,romance}`
- `--intensity {baja,media,alta}`
- `--summary-mode {neutral,viral_story}`
- `--editor-mode {narrativo,lista_escenas,highlights}`
- `--enable-tts`
- `--enable-monetization`
- `--target-duration` (20–90)
- `--language`
- `--vertical-format`
- `--output-dir`

## Uso del panel (Streamlit)

```bash
streamlit run app.py
```

En el panel:
- Sidebar: input video, mode, intensity, duración, enable TTS y enable monetization.
- Tabs: Transcripción, Resumen, Narrativa, Escenas, Matching, Clips y Final.
- Botón: **Ejecutar pipeline** para generar y visualizar artefactos.

## Salidas esperadas
`output/` contiene:
- `transcripts/transcript.json`
- `summaries/summary.json`
- `metadata/story_structure.json`
- `scripts/script_beats.json`
- `scenes/scene_candidates.json`
- `metadata/scene_matches.json`
- `metadata/timeline_plan.json`
- `clips/*.mp4`
- `edits/final_video.mp4`
- `metadata/monetization.json` (opcional)

## Limitaciones actuales (MVP)
- El análisis narrativo inicial es heurístico/extensible.
- El matching semántico usa `rapidfuzz` (rápido, sustituible por embeddings).
- Calidad final depende de audio/origen y codecs FFmpeg disponibles.

## Próximas mejoras
- Embeddings `transformers` para matching semántico profundo.
- Detección de acciones/objetos por frame para mayor coherencia visual.
- Ajuste de prosodia TTS por beat.
- Edición manual asistida desde el panel.
