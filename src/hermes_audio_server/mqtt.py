"""Helper functions to use the Paho MQTT library with the MQTT broker defined
in a :class:`.MQTTConfig` object.
"""


def connect(client, mqtt_config, keepalive=60, bind_address=''):
    """Connect to an MQTT broker with the MQTT connection settings defined in
    an :class:`.MQTTConfig` object.

    Args:
        client (:class:`paho.mqtt.client.Client`): The MQTT client object.
        mqtt_config (:class:`.MQTTConfig`): The MQTT connection settings.
        keepalive (int, optional): The maximum period in seconds allowed
            between communications with the broker. Defaults to 60.
        bind_address (str, optional): The IP address of a local network
            interface to bind this client to, assuming multiple interfaces
            exist. Defaults to ''.
    """
    # Set up MQTT authentication.
    if mqtt_config.auth.enabled:
        client.username_pw_set(mqtt_config.auth.username,
                               mqtt_config.auth.password)

    # Set up an MQTT TLS connection.
    if mqtt_config.tls.enabled:
        client.tls_set(ca_certs=mqtt_config.tls.ca_certs,
                       certfile=mqtt_config.tls.client_cert,
                       keyfile=mqtt_config.tls.client_key)

    client.connect(mqtt_config.host, mqtt_config.port, keepalive, bind_address)
