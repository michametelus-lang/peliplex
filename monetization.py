import logging
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s -
%(levelname)s - %(message)s')

def generate_monetization_data(summary: str) -> Dict[str, str]:
    """
    Generates viral title, description, and hashtags based on the
summary input.

    Parameters:
    - summary: str, input summary to generate monetization data from.

    Returns:
    - dict: dictionary containing 'title', 'description', and
'hashtags'.
    """
    try:
        # Generate viral title
        title = f"🔥 {summary.split('.')[0].strip().upper()} 🔥"

        # Generate description
        description = f"🚀 Dive into the thrilling world of
{summary.strip()}! Watch now and never miss out on this exciting
moment.\n\n#PeliPlex #ViralContent #Entertainment"

        # Generate hashtags
        hashtags = ["#PeliPlex", "#ViralContent", "#Entertainment"]

        for word in summary.split():
            if len(word) > 3:
                hashtags.append(f"#{word.capitalize()}")

        # Combine all data into a dictionary
        monetization_data = {
            "title": title,
            "description": description,
            "hashtags": ", ".join(hashtags)
        }

        logging.info("Monetization data generated successfully.")
        return monetization_data

    except Exception as e:
        logging.error(f"Error during monetization data generation:
{e}")
        return {}

# Example usage
if __name__ == "__main__":
    summary = "In the heart of the jungle, a group of adventurers
faces an unexpected challenge."

    monetization_data = generate_monetization_data(summary)
    print(monetization_data)
```

### Explanation:
- **Logging**: Configured to log information and errors.
- **Monetization Data Generation**:
  - **Title**: Generates a viral title using the first sentence of the
summary with an added emphasis using emojis.
  - **Description**: Creates a description highlighting the excitement
and encouraging viewers to watch the content. It also includes
relevant hashtags.
  - **Hashtags**: Includes a set of predefined hashtags along with
relevant keywords extracted from the summary.
- **Error Handling**: Includes basic error handling to ensure the
script can gracefully handle issues.
