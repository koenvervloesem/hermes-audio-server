"""Module with an MQTT client. Both the audio player and audio recorder class
inherit from this class.
"""
from paho.mqtt.client import Client


class MQTTClient:
    """This class represents an MQTT client for Hermes Audio Server.

    This is an abstract base class. You don't instantiate an object of this
    class, but an object of one of its subclasses.
    """

    def __init__(self, config, verbose):
        """Initialize an MQTT client.

        Args:
            config (:class:`.ServerConfig`): The configuration of
                the MQTT client.
            verbose (bool): Whether or not the MQTT client runs in verbose
                mode.
        """
        self.config = config
        self.verbose = verbose
        self.mqtt = Client()

        self.initialize()

        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect
        self.connect()

    def connect(self):
        """Connect to the MQTT broker defined in the configuration."""
        # Set up MQTT authentication.
        if self.config.mqtt.auth.enabled:
            self.mqtt.username_pw_set(self.config.mqtt.auth.username,
                                      self.config.mqtt.auth.password)

        # Set up an MQTT TLS connection.
        if self.config.mqtt.tls.enabled:
            self.mqtt.tls_set(ca_certs=self.config.mqtt.tls.ca_certs,
                              certfile=self.config.mqtt.tls.client_cert,
                              keyfile=self.config.mqtt.tls.client_key)

        self.mqtt.connect(self.config.mqtt.host, self.config.mqtt.port)

    def initialize(self):
        """Initialize the MQTT client."""

    def start(self):
        """Start the event loop to the MQTT broker so the audio server starts
        listening to MQTT topics and the callback methods are called.
        """
        self.mqtt.loop_forever()

    def on_connect(self, client, userdata, flags, result_code):
        """Callback that is called when the client connects to the MQTT broker.
        """
        print('Connected to MQTT broker {}:{}'
              ' with result code {}.'.format(self.config.mqtt.host,
                                             self.config.mqtt.port,
                                             result_code))

    def on_disconnect(self, client, userdata, flags, result_code):
        """Callback that is called when the client connects from the MQTT
        broker."""
        print('Disconnected with result code {}.'.format(result_code))
