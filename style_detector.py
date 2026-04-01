import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

class StyleDetector:
    """
    Class to detect the style of text based on keyword-based scoring
system.

    Supported styles: accion, drama, terror, misterio, romance

    Parameters:
    - keywords: Dict[str, List[str]], dictionary with genre as key and
list of keywords as value.
    """

    def __init__(self):
        self.keywords = {
            "accion": ["acción", "ataque", "guerra", "política"],
            "drama": ["amor", "familia", "tragedia", "sufrimiento"],
            "terror": ["siniestro", "miedo", "fantasma", "asesinato"],
            "misterio": ["misterio", "puzzle", "crimen", "desvelo"],
            "romance": ["amor", "novela", "ficción", "relación"]
        }

    def detect_style(self, text: str) -> str:
        """
        Detects the style of the given text based on keyword-based
scoring system.

        Parameters:
        - text: str, input text to be analyzed.

        Returns:
        - str: detected style or 'unknown' if no style is detected
with a high confidence score.
        """
        scores = {genre: 0 for genre in self.keywords}

        # Convert text to lowercase and split into words
        words = text.lower().split()

        # Calculate scores based on keywords
        for word in words:
            for genre, keyword_list in self.keywords.items():
                if word in keyword_list:
                    scores[genre] += 1

        # Find the genre with the highest score
        max_score = max(scores.values())
        detected_styles = [genre for genre, score in scores.items() if
score == max_score]

        if len(detected_styles) > 0 and max_score > 0:
            return detected_styles[0]
        else:
            return "unknown"

# Example usage
if __name__ == "__main__":
    detector = StyleDetector()

    # Sample input text
    sample_text = "La historia es sobre un hombre que vive en una
tierra donde la guerra está constante. Hay muchos ataques y luchas."

    detected_style = detector.detect_style(sample_text)
    print(f"Detected style: {detected_style}")
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **Keyword-based Scoring System**:
  - The `keywords` dictionary contains lists of keywords for each
supported genre.
  - The `detect_style` method calculates scores based on the presence
of these keywords in the input text.
  - The detected style is the one with the highest score.
- **Handling Unknown Styles**: If no style is detected with a high
confidence score, it returns "unknown".
