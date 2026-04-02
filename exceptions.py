"""Custom exceptions for PeliPlex."""

class PeliPlexError(Exception):
    """Base error for PeliPlex."""


class InvalidConfigurationError(PeliPlexError):
    """Raised when pipeline configuration is invalid."""


class VideoFileNotFoundError(PeliPlexError):
    """Raised when the input video file does not exist."""


class FFmpegNotInstalledError(PeliPlexError):
    """Raised when ffmpeg is not available in PATH."""


class VideoHasNoAudioError(PeliPlexError):
    """Raised when input video has no audio stream."""


class EmptyTranscriptionError(PeliPlexError):
    """Raised when transcription returns no meaningful text."""


class ModelLoadingError(PeliPlexError):
    """Raised when an ML model fails to load."""


class ClipExportError(PeliPlexError):
    """Raised when clip export fails."""


class TTSError(PeliPlexError):
    """Raised when text-to-speech generation fails."""
