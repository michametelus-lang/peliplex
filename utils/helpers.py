def split_long_text(text: str, max_chunk_length: int) -> List[str]:
    """
plits a long text into smaller chunks of a specified maximum
length.

    Parameters:
    - text: str, the input text to be split.
    - max_chunk_length: int, the maximum length of each chunk.

    Returns:
    - list: a list of string chunks.
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_chunk_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Example usage
if __name__ == "__main__":
    long_text = "This is a very long text that needs to be split into
smaller chunks for processing. Each chunk should not exceed the
maximum length specified."
    max_length = 50

    chunks = split_long_text(long_text, max_length)
    print(chunks)
```

### Explanation:
- **Functionality**:
  - The `split_long_text` function takes a string `text` and an
integer `max_chunk_length`.
  - It splits the text into smaller chunks where each chunk has a
length less than or equal to `max_chunk_length`.
  - Words are split at spaces, and punctuation is included in word
lengths.
- **Example Usage**:
  - The example demonstrates how to use the `split_long_text` function
to split a long string into chunks.
