import logging

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a reusable logger with a specific name, log level, and
format.

    Parameters:
    - name: str, the name of the logger.

    Returns:
    - logging.Logger: the configured logger.
    """
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the default log level to
DEBUG

    # Create a console handler and set its log level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Define a simple format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s -
%(levelname)s - %(message)s')

    # Set the formatter for the console handler
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    return logger

# Example usage
if __name__ == "__main__":
    logger = setup_logger("my_logger")
    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
```

### Explanation:
- **Logging Configuration**:
  - The `setup_logger` function configures a logger with the specified
name.
  - It sets the default log level to `DEBUG`, meaning all levels of
logs (DEBUG, INFO, WARNING, ERROR, CRITICAL) will be captured.
  - A console handler is added to output logs to the console.
  - A simple format is defined for log messages that includes the
timestamp, logger name, log level, and message.
- **Reusability**:
  - The `setup_logger` function returns a configured logger that can
be easily imported and used in other parts of your application.

### Usage Example:
To use this logger in another part of your application, you can import
the `setup_logger` function and create a logger instance:

```python
from logger import setup_logger

logger = setup_logger("my_application")
logger.info("This is an info message from my_application.")
```

This will log the message to the console with the specified format.
