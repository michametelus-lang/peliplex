import os
import logging
from datetime import timedelta
from moviepy.editor import VideoFileClip
import whisper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

# Load a lightweight model (small)
model = whisper.load_model("tiny")

def transcribe_video(video_path):
    """
    Transcribes a video file using the OpenAI Whisper library.

    Parameters:
    - video_path: str, path to the input video file.

    Returns:
    - list of dictionaries: [{ "start": float, "end": float, "text":
string }]
    """
    try:
        # Check if the video file exists
        if not os.path.exists(video_path):
            logging.error(f"Video file '{video_path}' does not
exist.")
            return []

        # Load the video clip using moviepy
        clip = VideoFileClip(video_path)
        duration = clip.duration

        # Initialize an empty list to store transcription results
        transcriptions = []

        # Split the video into chunks for processing
        chunk_size = int(duration / 10)  # Process in 10-second chunks
for efficiency
        for start_time in range(0, duration, chunk_size):
            end_time = min(start_time + chunk_size, duration)
            chunk_clip = clip.subclip(start_time, end_time)

            # Transcribe the current chunk
            result = model.transcribe(chunk_clip.audio_path)
            segments = result['segments']

            for segment in segments:
                transcriptions.append({
                    "start": start_time + segment['start'],
                    "end": start_time + segment['end'],
                    "text": segment['text'].strip()
                })

        # Remove overlapping or duplicate entries
        unique_transcriptions = []
        previous_end = 0.0
        for transcription in transcriptions:
            if transcription["start"] > previous_end:
                unique_transcriptions.append(transcription)
                previous_end = transcription["end"]

        logging.info(f"Transcription completed successfully.")
        return unique_transcriptions

    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return []

# Example usage
if __name__ == "__main__":
    video_path = "path/to/input/video.mp4"
    transcriptions = transcribe_video(video_path)

    for transcription in transcriptions:
        print(transcription)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle missing files or other issues.
- **Model Loading**: Uses a lightweight model (`tiny`) from OpenAI
Whisper for efficient processing.
- **Transcription Function**: `transcribe_video` function that:
  - Loads the video clip using moviepy.
  - Splits the video into 10-second chunks to optimize processing for
long videos.
  - Transcribes each chunk using the Whisper model.
  - Removes overlapping or duplicate transcriptions.
