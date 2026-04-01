import logging
from typing import str

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

def generate_voice(text: str, output_file: str) -> None:
    """
    Converts the given text into speech and saves it as an audio file.

    Parameters:
    - text: str, input text to be converted into speech.
    - output_file: str, path where the output audio file will be
saved.

    Returns:
    - None
    """
    try:
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set properties before adding anything to speak
        rate = engine.getProperty('rate')  # getting details of
current speaking rate
        volume = engine.getProperty('volume')   # getting to know
current volume level (min=0 and max=1)
        voices = engine.getProperty('voices')   # getting details of
current voice

        # Set properties before adding anything to speak
        engine.setProperty('rate', 150)     # setting up new voice
rate
        engine.setProperty('volume', 1.0)   # setting volume 0-1
        engine.setProperty('voice', voices[0].id)  # change voices

        # Adding things to say
        engine.say(text)

        # Blocks while processing all the commands queued in the
VoiceCommand queue.
        engine.runAndWait()

        # Saving the speech to a file
        engine.save_to_file(text, output_file)
        engine.runAndWait()

        logging.info(f"Audio saved: {output_file}")

    except Exception as e:
        logging.error(f"Error during text-to-speech conversion: {e}")

# Example usage
if __name__ == "__main__":
    input_text = "Hello, this is a test of the text-to-speech
functionality."
    output_audio_file = "outputs/test_output.wav"

    generate_voice(input_text, output_audio_file)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **pyttsx3 Integration**:
  - The `pyttsx3` library is used to initialize the text-to-speech
engine.
  - Text is converted into speech and saved as an audio file.
  - Properties such as rate, volume, and voice can be customized.
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle issues.
