import logging
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

def split_video(input_video_path: str, output_folder: str,
chunk_duration: float = 300.0) -> List[str]:
    """
    Splits a long video into smaller chunks of specified duration.

    Parameters:
    - input_video_path: str, the path to the input video file.
    - output_folder: str, the folder where chunk files will be saved.
    - chunk_duration: float, the desired duration for each chunk in
seconds (default is 300 seconds or 5 minutes).

    Returns:
    - list: a list of file paths to the created chunk videos.
    """
    try:
        # Load the input video
        video_clip = VideoFileClip(input_video_path)

        if not video_clip:
            logging.error("Failed to load input video.")
            return []

        total_duration = video_clip.duration
        num_chunks = int(total_duration / chunk_duration) + 1

        chunks = []

        for i in range(num_chunks):
            start_time = i * chunk_duration
            end_time = min((i + 1) * chunk_duration, total_duration)

            # Extract the current chunk
            chunk_clip = video_clip.subclip(start_time, end_time)

            # Define output path for the chunk
            output_path = f"{output_folder}/chunk_{i:03d}.mp4"

            # Write the chunk to a file
            chunk_clip.write_videofile(output_path, codec='libx264')

            logging.info(f"Chunk saved: {output_path}")

            chunks.append(output_path)

        return chunks

    except Exception as e:
        logging.error(f"Error during video splitting: {e}")
        return []

# Example usage
if __name__ == "__main__":
    input_video_path = "inputs/long_video.mp4"
    output_folder = "outputs/chunks/"

    chunk_paths = split_video(input_video_path, output_folder)
    print(chunk_paths)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **MoviePy Integration**:
  - The `VideoFileClip` class from MoviePy is used to load the input
video.
  - The video is split into smaller chunks based on the specified
`chunk_duration`.
  - Each chunk is saved as a separate video file in the provided
output folder.
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle issues.
