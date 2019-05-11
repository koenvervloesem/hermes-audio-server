"""Module with the Hermes audio player class."""
import io
import json
import wave

from humanfriendly import format_size
from paho.mqtt.client import Client
import pyaudio

from hermes_audio_server.mqtt import connect

PLAY_BYTES = 'hermes/audioServer/{}/playBytes/+'
PLAY_FINISHED = 'hermes/audioServer/{}/playFinished'
CHUNK = 256


class AudioPlayer:
    """This class creates an MQTT client that acts as an audio player for the
    Hermes protocol.
    """

    def __init__(self, config, verbose):
        """Initialize a Hermes audio player.

        Args:
            config (:class:`.ServerConfig`): The configuration of
                the Hermes audio player.
        """
        self.config = config
        self.verbose = verbose
        self.mqtt = Client()
        print('Audio player created on site {}.'.format(self.config.site))

        self.audio = pyaudio.PyAudio()
        self.audio_out = self.audio.get_default_output_device_info()['name']
        print('Connected to audio output {}.'.format(self.audio_out))

        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect

        connect(self.mqtt, self.config.mqtt)

    def start(self):
        """Start the event loop to the MQTT broker so the audio player starts
        listening to MQTT topics and the callback methods are called.
        """
        self.mqtt.loop_forever()

    def on_connect(self, client, userdata, flags, result_code):
        print('Connected to MQTT broker {}:{}'
              ' with result code {}.'.format(self.config.mqtt.host,
                                             self.config.mqtt.port,
                                             result_code))

        play_bytes = PLAY_BYTES.format(self.config.site)
        self.mqtt.subscribe(play_bytes)
        self.mqtt.message_callback_add(play_bytes, self.on_play_bytes)
        print('Subscribed to {}.'.format(play_bytes))

    def on_disconnect(self, client, userdata, flags, result_code):
        print('Disconnected with result code {}.'.format(result_code))

    def on_play_bytes(self, client, userdata, message):
        request_id = message.topic.split('/')[4]
        length = format_size(len(message.payload), binary=True)
        print('Received an audio message of length {}'
              ' with request id {} on site {}.'.format(length,
                                                       request_id,
                                                       self.config.site))

        with io.BytesIO(message.payload) as wav_buffer:
            with wave.open(wav_buffer, 'rb') as wav:
                sample_width = wav.getsampwidth()
                sample_format = self.audio.get_format_from_width(sample_width)
                n_channels = wav.getnchannels()
                frame_rate = wav.getframerate()

                if self.verbose:
                    print('Sample width: {}'.format(sample_width))
                    print('Channels: {}'.format(n_channels))
                    print('Frame rate: {}'.format(frame_rate))

                stream = self.audio.open(format=sample_format,
                                         channels=n_channels,
                                         rate=frame_rate,
                                         output=True)

                data = wav.readframes(CHUNK)

                while len(data) > 0:
                    stream.write(data)
                    data = wav.readframes(CHUNK)

                stream.stop_stream()
                stream.close()

        self.mqtt.publish(PLAY_FINISHED.format(self.config.site),
                          json.dumps({'id': request_id,
                                      'siteId': self.config.site}))
        print('Finished playing audio message with id {}'
              ' on device {} on site {}'.format(request_id,
                                                self.audio_out,
                                                self.config.site))
