"""Class for the VAD configuration of hermes-audio-server."""

# Default values
DEFAULT_MODE = 0
DEFAULT_SEND_MESSAGES = False

# Keys in the JSON configuration file
MODE = 'mode'
SEND_MESSAGES = 'send_messages'


# TODO: Define __str__() for each class with explicit settings for debugging.
class VADConfig:
    """This class represents the VAD settings for Hermes Audio Recorder.

    Attributes:
        enabled (bool): Whether or not VAD is enabled.
        mode (int): Aggressiveness mode for VAD. 0 is the least aggressive
            about filtering out non-speech, 3 is the most aggressive.
        send_messages (bool): Whether or not Hermes Audio Recorder sends
             messages on MQTT when it detects the start or end of a voice
             message.
    """

    def __init__(self, enabled=False, mode=0, send_messages=False):
        """Initialize a :class:`.VADConfig` object.

        Args:
            enabled (bool): Whether or not VAD is enabled. Defaults to False.
            mode (int): Aggressiveness mode for VAD. Defaults to 0.
            send_messages (bool): Whether or not Hermes Audio Recorder sends
                messages on MQTT when it detects the start or end of a voice
                message. Defaults to False.

        All arguments are optional.
        """
        self.enabled = enabled
        self.mode = mode
        self.send_messages = send_messages

    @classmethod
    def from_json(cls, json_object=None):
        """Initialize a :class:`.VADConfig` object with settings from a
        JSON object.

        Args:
            json_object (optional): The JSON object with the VAD settings.
                Defaults to {}.

        Returns:
            :class:`.VADConfig`: An object with the VAD settings.

        The JSON object should have the following format:

        {
            "mode": 0,
            "send_messages": true
        }
        """
        if json_object is None:
            return cls(enabled=False)
        else:
            return cls(enabled=True,
                       mode=json_object.get(MODE, DEFAULT_MODE),
                       send_messages=json_object.get(SEND_MESSAGES,
                                                     DEFAULT_SEND_MESSAGES))
