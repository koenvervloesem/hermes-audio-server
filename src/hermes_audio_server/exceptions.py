"""This module contains exceptions defined for Hermes Audio Server."""


class HermesAudioServerError(Exception):
    """Base class for exceptions raised by Hermes Audio Server code.

    By catching this exception type, you catch all exceptions that are
    defined by the Hermes Audio Server code."""


class ConfigurationFileNotFoundError(HermesAudioServerError):
    """Raised when the configuration file is not found."""

    def __init__(self, filename):
        """Initialize the exception with a string representing the filename."""
        self.filename = filename


class NoDefaultAudioDeviceError(HermesAudioServerError):
    """Raised when there's no default audio device available."""

    def __init__(self, inout):
        """Initialize the exception with a string representing input or output.
        """
        self.inout = inout


class UnsupportedPlatformError(HermesAudioServerError):
    """Raised when the platform Hermes Audio Server is running on is not
    supported."""

    def __init__(self, platform):
        """Initialize the exception with a string representing the platform."""
        self.platform = platform
