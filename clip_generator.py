import logging
from typing import List, Dict
from moviepy.editor import VideoFileClip

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

class ClipGenerator:
    """
    Class to generate clips from detected scenes using MoviePy.

    Parameters:
    - input_video_path: str, path to the input video file.
    - output_folder: str, folder where generated clips will be saved.
    """

    def __init__(self, input_video_path: str, output_folder: str):
        self.input_video_path = input_video_path
        self.output_folder = output_folder

    def generate_clips(self, scenes: List[Dict[str, float]],
intensity: str) -> None:
        """
        Generates clips from detected scenes and saves them to the
specified folder.

        Parameters:
        - scenes: List[Dict[str, float]], list of dictionaries with
'start' and 'end' timestamps for each scene.
        - intensity: str, intensity level ('high' or 'low').

        Returns:
        - None
        """
        try:
            # Load the input video
            video_clip = VideoFileClip(self.input_video_path)

            # Calculate clip duration based on intensity
            if intensity == "high":
                min_duration = 1.0
            elif intensity == "low":
                min_duration = 3.0
            else:
                raise ValueError("Invalid intensity level. Choose
either 'high' or 'low'.")

            # Generate clips from detected scenes
            for i, scene in enumerate(scenes):
                start_time = scene['start']
                end_time = scene['end']

                if end_time - start_time >= min_duration:
                    clip = video_clip.subclip(start_time, end_time)
                    output_path = f"{self.output_folder}/clip_{i}.mp4"
                    clip.write_videofile(output_path, codec='libx264')
                    logging.info(f"Clip saved: {output_path}")
                else:
                    logging.warning(f"Skipping short clip at time
{start_time} to {end_time}")

        except Exception as e:
            logging.error(f"Error during clip generation: {e}")

# Example usage
if __name__ == "__main__":
    input_video_path = "path/to/your/input/video.mp4"
    output_folder = "outputs/clips/"

    # Sample input scenes with start and end timestamps
    sample_scenes = [
        {"start": 0, "end": 10},
        {"start": 30, "end": 50},
        {"start": 70, "end": 90}
    ]

    intensity = "high"

    generator = ClipGenerator(input_video_path, output_folder)
    generator.generate_clips(sample_scenes, intensity)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **MoviePy Integration**:
  - The `VideoFileClip` class from MoviePy is used to load the input
video.
  - Clips are generated based on detected scenes with start and end
timestamps.
  - Clips shorter than 2 seconds (or based on intensity) are skipped.
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle issues.
