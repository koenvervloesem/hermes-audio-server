"""Classes for the configuration of hermes-audio-server."""
import json
from pathlib import Path

from hermes_audio_server.config.mqtt import MQTTConfig


# Default values
DEFAULT_CONFIG = '/etc/hermes-audio-server.json'
DEFAULT_SITE = 'default'

# Keys in the JSON configuration file
SITE = 'site'
MQTT = 'mqtt'


# TODO: Define __str__() with explicit settings for debugging.
class ServerConfig:
    """This class represents the configuration of a Hermes audio server.

    Attributes:
        site (str): The site ID of the audio server.
        mqtt (:class:`.MQTTConfig`): The MQTT options of the configuration.
    """

    def __init__(self, site='default', mqtt=None):
        """Initialize a :class:`.ServerConfig` object.

        Args:
            site (str): The site ID of the Hermes audio server. Defaults
                to 'default'.
            mqtt (:class:`.MQTTConfig`, optional): The MQTT connection
                settings. Defaults to a default :class:`.MQTTConfig` object.
        """
        if mqtt is None:
            self.mqtt = MQTTConfig()
        else:
            self.mqtt = mqtt

        self.site = site

    @classmethod
    def from_json_file(cls, filename=None):
        """Initialize a :class:`.ServerConfig` object with settings
        from a JSON file.

        Args:
            filename (str): The filename of a JSON file with the settings.
                Defaults to '/etc/hermes-audio-server'.

        Returns:
            :class:`.ServerConfig`: An object with the settings
            of the Hermes Audio Server.

        The :attr:`mqtt` attribute of the :class:`.ServerConfig`
        object is initialized with the MQTT connection settings from the
        configuration file, or the default values (hostname 'localhost' and
        port number 1883) if the settings are not specified.

        The :attr:`site` attribute of the :class:`.ServerConfig`
        object is initialized with the setting from the configuration file,
        or 'default' is the setting is not specified.

        Raises:
            :exc:`FileNotFoundError`: If :attr:`filename` doesn't exist.

            :exc:`JSONDecodeError`: If :attr:`filename` doesn't have a valid
                JSON syntax.

        The JSON file should have the following format:

        {
            "site": "default",
            "mqtt": {
                "host": "localhost",
                "port": 1883,
                "authentication": {
                    "username": "foobar",
                    "password": "secretpassword"
                },
                "tls": {
                    "ca_certificates": "",
                    "client_certificate": "",
                    "client_key": ""
                }
            }
        }
        """
        if not filename:
            filename = DEFAULT_CONFIG

        try:
            with Path(filename).open('r') as json_file:
                configuration = json.load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError('{} not found'.format(filename))

        return cls(site=configuration.get(SITE, DEFAULT_SITE),
                   mqtt=MQTTConfig.from_json(configuration.get(MQTT)))
