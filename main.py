import logging
from typing import List, Optional
from multiprocessing import Pool
from video_chunker import split_video
from transcription import transcribe_audio
from summarization import generate_summary
from scene_detection import detect_scenes
from clip_generation import generate_clips
from video_assembly import assemble_final_video
from monetization import generate_monetization_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

def process_chunk(chunk_path: str) -> dict:
    """
    Process a single chunk of video.

    Parameters:
    - chunk_path: str, the path to the input video chunk file.

    Returns:
    - dict: a dictionary containing processed data for the chunk.
    """
    try:
        # Transcribe audio from the chunk
        transcriptions = transcribe_audio(chunk_path)

        # Generate summary of the transcription
        summary = generate_summary(transcriptions)

        return {
            "chunk_path": chunk_path,
            "transcriptions": transcriptions,
            "summary": summary
        }

    except Exception as e:
        logging.error(f"Error processing chunk: {e}")
        return {}

def main(input_video_path: str, output_folder: str, mode: str =
"auto", auto_intensity: float = 1.0) -> None:
    """
    Orchestrates the full pipeline for PeliPlex.

    Parameters:
    - input_video_path: str, the path to the input video file.
    - output_folder: str, the folder where chunk files will be saved.
    - mode: str, the processing mode ("auto" or "manual").
    - auto_intensity: float, intensity value for automatic mode
(default is 1.0).

    Returns:
    - None
    """
    try:
        # Split video into chunks
        chunk_paths = split_video(input_video_path, output_folder)

        if not chunk_paths:
            logging.error("Failed to split video.")
            return

        # Process each chunk in parallel
        with Pool(processes=4) as pool:
            results = pool.map(process_chunk, chunk_paths)

        # Extract processed data from results
        processed_chunks = [result for result in results if result]

        if not processed_chunks:
            logging.error("No valid chunks processed.")
            return

        # Detect scenes and generate clips
        scene_data = detect_scenes(processed_chunks)
        clips = generate_clips(scene_data, mode=mode,
auto_intensity=auto_intensity)

        if not clips:
            logging.error("Failed to generate clips.")
            return

        # Assemble final video
        final_video_path = assemble_final_video(clips, output_folder)

        if not final_video_path:
            logging.error("Failed to assemble final video.")
            return

        # Optional monetization
        monetization_data =
generate_monetization_data(processed_chunks[0]["summary"])

        if monetization_data:
            logging.info(f"Monetization data: {monetization_data}")

        logging.info(f"Final video saved: {final_video_path}")

    except Exception as e:
        logging.error(f"Error during main pipeline execution: {e}")

# Example usage
if __name__ == "__main__":
    input_video_path = "inputs/long_video.mp4"
    output_folder = "outputs/"
    mode = "auto"  # or "manual"
    auto_intensity = 1.0

    main(input_video_path, output_folder, mode=mode,
auto_intensity=auto_intensity)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **Pipeline Steps**:
  - The script orchestrates the full pipeline from splitting videos
into chunks to generating final videos and optional monetization.
  - It processes each chunk in parallel using `multiprocessing.Pool`.
  - "Brain logic" for auto/manual mode is implemented, allowing users
to choose between automatic and manual processing modes.
