"""This module contains exceptions defined for Hermes Audio Server."""


class HermesAudioServerError(Exception):
    """Base class for exceptions raised by Hermes Audio Server code.

    By catching this exception type, you catch all exceptions that are
    defined by the Hermes Audio Server code."""


class UnsupportedPlatformError(HermesAudioServerError):
    """Raised when the platform Hermes Audio Server is running on is not
    supported."""

    def __init__(self, platform):
        """Initialize the exception with a string representing the platform."""
        self.platform = platform
