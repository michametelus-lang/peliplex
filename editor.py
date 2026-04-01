import logging
from typing import List, Dict
from moviepy.editor import concatenate_videoclips

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

class VideoEditor:
    """
    Class to combine clips into a final video using MoviePy.

    Parameters:
    - input_clips: List[str], list of paths to input clip files.
    - output_folder: str, folder where the final video will be saved.
    """

    def __init__(self, input_clips: List[str], output_folder: str):
        self.input_clips = input_clips
        self.output_folder = output_folder

    def combine_clips(self, mode: str) -> None:
        """
        Combines clips into a final video based on the specified mode.

        Parameters:
        - mode: str, combination mode ('narrative', 'list', or
'highlights').

        Returns:
        - None
        """
        try:
            # Load input clips
            clips = [VideoFileClip(clip_path) for clip_path in
self.input_clips]

            if not clips:
                logging.error("No clips to combine.")
                return

            # Sort clips based on mode
            if mode == "narrative":
                pass  # Keep clips in their original order
            elif mode == "list":
                clips.sort(key=lambda clip: len(clip))
            elif mode == "highlights":
                clips.sort(key=lambda clip: len(clip), reverse=True)
            else:
                raise ValueError("Invalid combination mode. Choose
either 'narrative', 'list', or 'highlights'.")

            # Combine clips
            final_clip = concatenate_videoclips(clips,
method="compose")

            # Define output path
            output_path = f"{self.output_folder}/final_video.mp4"
            final_clip.write_videofile(output_path, codec='libx264')
            logging.info(f"Final video saved: {output_path}")

        except Exception as e:
            logging.error(f"Error during video combination: {e}")

# Example usage
if __name__ == "__main__":
    input_clips = [
        "outputs/clips/clip_0.mp4",
        "outputs/clips/clip_1.mp4",
        "outputs/clips/clip_2.mp4"
    ]

    output_folder = "outputs/final/"

    editor = VideoEditor(input_clips, output_folder)
    editor.combine_clips("narrative")
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **MoviePy Integration**:
  - The `VideoFileClip` class from MoviePy is used to load input
clips.
  - Clips are combined based on the specified mode:
    - "narrative": Keeps clips in their original order.
    - "list": Sorts clips by length (shortest first).
    - "highlights": Sorts clips by length (longest first).
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle issues.
