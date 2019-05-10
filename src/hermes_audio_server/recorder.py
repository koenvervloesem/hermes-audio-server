"""Module with the Hermes audio recorder class."""
import io
from threading import Thread
import wave

from paho.mqtt.client import Client
import pyaudio

from mqtt import connect

AUDIO_FRAME = 'hermes/audioServer/{}/audioFrame'
CHANNELS = 1
CHUNK = 256
FRAME_RATE = 16000
SAMPLE_WIDTH = 2


# TODO: Call stream.stop_stream() and stream.close()
class AudioRecorder:
    """This class creates an MQTT client that acts as an audio recorder for the
    Hermes protocol.
    """

    def __init__(self, config, verbose):
        """Initialize a Hermes audio recorder.

        Args:
            config (:class:`.ServerConfig`): The configuration of
                the Hermes audio recorder.
        """
        self.config = config
        self.verbose = verbose
        self.mqtt = Client()
        print('Audio recorder created on site {}.'.format(self.config.site))

        self.audio = pyaudio.PyAudio()
        self.audio_in = self.audio.get_default_input_device_info()['name']
        print('Connected to audio input {}.'.format(self.audio_in))

        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect

        connect(self.mqtt, self.config.mqtt)

    def start(self):
        """Start the event loop to the MQTT broker and start the audio
        recording."""
        Thread(target=self.send_audio_frames, daemon=True).start()
        self.mqtt.loop_forever()

    def on_connect(self, client, userdata, flags, result_code):
        print('Connected to MQTT broker {}:{}'
              ' with result code {}.'.format(self.config.mqtt.host,
                                             self.config.mqtt.port,
                                             result_code))

    def on_disconnect(self, client, userdata, flags, result_code):
        print('Disconnected with result code {}.'.format(result_code))

    def send_audio_frames(self):
        stream = self.audio.open(format=pyaudio.paInt16, channels=CHANNELS,
                                 rate=FRAME_RATE, input=True,
                                 frames_per_buffer=CHUNK)

        print('Started broadcasting audio from device {}'
              ' on site {}'.format(self.audio_in, self.config.site))

        while True:
            frames = stream.read(CHUNK, exception_on_overflow=False)
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wav:
                    # pylint: disable=no-member
                    wav.setnchannels(CHANNELS)
                    wav.setsampwidth(SAMPLE_WIDTH)
                    wav.setframerate(FRAME_RATE)
                    wav.writeframes(frames)
                self.mqtt.publish(AUDIO_FRAME.format(self.config.site),
                                  wav_buffer.getvalue())
