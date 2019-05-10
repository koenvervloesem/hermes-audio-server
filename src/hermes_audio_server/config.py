"""Classes for the configuration of hermes-audio-server."""
import json
from pathlib import Path


# Default values
DEFAULT_CONFIG = '/etc/hermes-audio-server.json'
DEFAULT_SITE = 'default'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 1883

# Keys in the JSON configuration file
SITE = 'site'
MQTT = 'mqtt'
HOST = 'host'
PORT = 'port'
AUTH = 'authentication'
USERNAME = 'username'
PASSWORD = 'password'
TLS = 'tls'
CA_CERTS = 'ca_certificates'
CLIENT_CERT = 'client_certificate'
CLIENT_KEY = 'client_key'


# TODO: Define __str__() for each class with explicit settings for debugging.
class MQTTAuthConfig:
    """This class represents the authentication settings for a connection to an
    MQTT broker.

    Attributes:
        username (str): The username to authenticate to the MQTT broker. `None`
            if there's no authentication.
        password (str): The password to authenticate to the MQTT broker. Can be
            `None`.
    """

    def __init__(self, username=None, password=None):
        """Initialize a :class:`.MQTTAuthConfig` object.

        Args:
            username (str, optional): The username to authenticate to the MQTT
                broker. `None` if there's no authentication.
            password (str, optional): The password to authenticate to the MQTT
                broker. Can be `None`.

        All arguments are optional.
        """
        self.username = username
        self.password = password

    @classmethod
    def from_json(cls, json_object=None):
        """Initialize a :class:`.MQTTAuthConfig` object with settings from a
        JSON object.

        Args:
            json_object (optional): The JSON object with the MQTT
                authentication settings. Defaults to {}.

        Returns:
            :class:`.MQTTAuthConfig`: An object with the MQTT authentication
            settings.

        The JSON object should have the following format:

        {
            "username": "foobar",
            "password": "secretpassword"
        }
        """
        if json_object is None:
            json_object = {}

        return cls(username=json_object.get(USERNAME),
                   password=json_object.get(PASSWORD))

    @property
    def enabled(self):
        """Check whether authentication is enabled.

        Returns:
            bool: True if the username is not `None`.
        """
        return self.username is not None


class MQTTTLSConfig:
    """This class represents the TLS settings for a connection to an MQTT
    broker.

    Attributes:
        enabled (bool): Whether or not TLS is enabled.
        ca_certs (str): Path to the Certificate Authority file. If `None`, the
            default certification authority of the system is used.
        client_key (str): Path to an PEM encoded private key file. If `None`,
            there will be no client authentication.
        client_cert (str): Path to a PEM encoded client certificate file. If
            `None`, there will be no client authentication.
    """

    def __init__(self, enabled=False, ca_certs=None, client_key=None,
                 client_cert=None):
        """Initialize a :class:`.MQTTTLSConfig` object.

        Args:
            enabled (bool, optional): Whether or not TLS is enabled. The
                default value is `False`.
            ca_certs (str, optional): Path to the Certificate Authority file.
                If `None`, the default certification authority of the system is
                used.
            client_key (str, optional): Path to a PEM encoded private key file.
                If `None`, there will be no client authentication.
            client_cert (str, optional): Path to a PEM encoded client
                certificate file. If `None`, there will be no client
                authentication.

        All arguments are optional.
        """
        self.enabled = enabled
        self.ca_certs = ca_certs
        self.client_key = client_key
        self.client_cert = client_cert

    @classmethod
    def from_json(cls, json_object=None):
        """Initialize a :class:`.MQTTTLSConfig` object with settings from a
        JSON object.

        Args:
            json_object (optional): The JSON object with the MQTT TLS settings.
                Defaults to {}.

        Returns:
            :class:`.MQTTTLSConfig`: An object with the MQTT TLS settings.

        The JSON object should have the following format:

        {
            "ca_certificates": "",
            "client_certificate": "",
            "client_key": ""
        }
        """
        if json_object is None:
            return cls(enabled=False)
        else:
            return cls(enabled=True,
                       ca_certs=json_object.get(CA_CERTS),
                       client_key=json_object.get(CLIENT_KEY),
                       client_cert=json_object.get(CLIENT_CERT))


class MQTTConfig:
    """This class represents the configuration for a connection to an
    MQTT broker.

    Attributes:
        host (str): The hostname or IP address of the MQTT broker.
        port (int): The port number  of the MQTT broker.
        auth (:class:`.MQTTAuthConfig`, optional): The authentication
            settings (username and password) for the MQTT broker.
        tls (:class:`.MQTTTLSConfig`, optional): The TLS settings for the MQTT
            broker.
    """

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, auth=None,
                 tls=None):
        """Initialize a :class:`.MQTTConfig` object.

        Args:
            host (str, optional): The hostname or IP address of the MQTT
                broker.
            port (int, optional): The port number of the MQTT broker.
            auth (:class:`.MQTTAuthConfig`, optional): The authentication
                settings (username and password) for the MQTT broker. Defaults
                to a default :class:`.MQTTAuthConfig` object.
            tls (:class:`.MQTTTLSConfig`, optional): The TLS settings for the
                MQTT broker. Defaults to a default :class:`.MQTTTLSConfig`
                object.

        All arguments are optional.
        """
        self.host = host
        self.port = port

        if auth is None:
            self.auth = MQTTAuthConfig()
        else:
            self.auth = auth

        if tls is None:
            self.tls = MQTTTLSConfig()
        else:
            self.tls = tls

    @classmethod
    def from_json(cls, json_object=None):
        """Initialize a :class:`.MQTTConfig` object with settings from a JSON
        object.

        Args:
            json_object (optional): The JSON object with the MQTT settings.
                Defaults to {}.

        Returns:
            :class:`.MQTTConfig`: An object with the MQTT settings.

        The JSON object should have the following format:

        {
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
        """
        if json_object is None:
            json_object = {}

        return cls(host=json_object.get(HOST, DEFAULT_HOST),
                   port=json_object.get(PORT, DEFAULT_PORT),
                   auth=MQTTAuthConfig.from_json(json_object.get(AUTH)),
                   tls=MQTTTLSConfig.from_json(json_object.get(TLS)))


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
