class Config:
    """
    Configuration settings for PeliPlex project.

    Parameters:
    - MODE (str): Operation mode ('auto' or 'manual').
    - STYLE (str): Video style ('accion', 'drama', 'terror',
'misterio', 'romance').
    - INTENSITY (str): Video intensity level ('low', 'medium',
'high').
    - MIN_CLIP_DURATION (int): Minimum clip duration in
seconds.
    - MAX_CLIP_DURATION (int): Maximum clip duration in seconds.
    - ENABLE_TTS (bool): Enable Text-to-Speech feature.
    - ENABLE_MONETIZATION (bool): Enable monetization feature.
    - INPUT_VIDEO (str): Path to the input video file.
    - OUTPUT_DIR (str): Folder path for output files.
    - CHUNK_DURATION (int): Duration in seconds for splitting long
videos into chunks.
    """

    MODE = "auto"  # Operation mode, can be 'auto' or 'manual'

    STYLE = "drama"  # Video style, e.g., accion, drama, terror,
misterio, romance

    INTENSITY = "medium"  # Video intensity level, e.g., low, medium,
high

    MIN_CLIP_DURATION = 60  # Minimum clip duration in seconds (e.g.,
60 seconds)

    MAX_CLIP_DURATION = 120  # Maximum clip duration in seconds (e.g.,
120 seconds)

    ENABLE_TTS = True  # Enable Text-to-Speech feature, set to False
if not needed

    ENABLE_MONETIZATION = True  # Enable monetization feature, set to
False if not needed

    INPUT_VIDEO = "path/to/input/video.mp4"  # Path to the input video
file

    OUTPUT_DIR = "output/videos/"  # Folder path for output files

    CHUNK_DURATION = 300  # Duration in seconds for splitting long
videos into chunks (e.g., 5 minutes)

# Example usage
if __name__ == "__main__":
    config = Config()
    print(f"MODE: {config.MODE}")
    print(f"STYLE: {config.STYLE}")
    print(f"INTENSITY: {config.INTENSITY}")
    print(f"MIN_CLIP_DURATION: {config.MIN_CLIP_DURATION} seconds")
    print(f"MAX_CLIP_DURATION: {config.MAX_CLIP_DURATION} seconds")
    print(f"ENABLE_TTS: {config.ENABLE_TTS}")
    print(f"ENABLE_MONETIZATION: {config.ENABLE_MONETIZATION}")
    print(f"INPUT_VIDEO: {config.INPUT_VIDEO}")
    print(f"OUTPUT_DIR: {config.OUTPUT_DIR}")
    print(f"CHUNK_DURATION: {config.CHUNK_DURATION} seconds")
```

### Explanation:
- **MODE**: Specifies whether the system operates in automatic
(`auto`) or manual (`manual`) mode.
- **STYLE**: Defines the video genre style, which can be one of
'accion', 'drama', 'terror', 'misterio', 'romance'.
- **INTENSITY**: Sets the intensity level of the video content, either
'low', 'medium', or 'high'.
- **MIN_CLIP_DURATION** and **MAX_CLIP_DURATION**: Define the minimum
and maximum duration for each clip in seconds.
- **ENABLE_TTS**: A boolean indicating whether Text-to-Speech
functionality is enabled.
- **ENABLE_MONETIZATION**: A boolean indicating whether monetization
features are enabled.
- **INPUT_VIDEO**: The file path to the input video that needs
processing.
- **OUTPUT_DIR**: The directory where processed videos and other
outputs will be stored.
- **CHUNK_DURATION**: Defines the duration (in seconds) for splitting
long videos into smaller chunks.
