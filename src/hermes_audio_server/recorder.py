"""Module with the Hermes audio recorder class."""
import io
import json
from threading import Thread
import wave

import pyaudio
import webrtcvad

from hermes_audio_server.mqtt import MQTTClient

AUDIO_FRAME = 'hermes/audioServer/{}/audioFrame'
CHANNELS = 1
CHUNK = 320  # = FRAME_RATE * 20 / 1000 (20 ms)
FRAME_RATE = 16000
SAMPLE_WIDTH = 2

VAD_DOWN = 'hermes/voiceActivity/{}/vadDown'
VAD_UP = 'hermes/voiceActivity/{}/vadUp'


# TODO: Call stream.stop_stream() and stream.close()
class AudioRecorder(MQTTClient):
    """This class creates an MQTT client that acts as an audio recorder for the
    Hermes protocol.
    """

    def initialize(self):
        """Initialize a Hermes audio recorder."""
        self.audio = pyaudio.PyAudio()
        self.audio_in = self.audio.get_default_input_device_info()['name']
        print('Connected to audio input {}.'.format(self.audio_in))

        if self.config.vad.enabled:
            print('Voice Activity Detection enabled with mode {}'.format(self.config.vad.mode))
            self.vad = webrtcvad.Vad(self.config.vad.mode)

    def start(self):
        """Start the event loop to the MQTT broker and start the audio
        recording."""
        Thread(target=self.send_audio_frames, daemon=True).start()
        super(AudioRecorder, self).start()

    def publish_frames(self, frames):
        """Publish frames on MQTT."""
        with io.BytesIO() as wav_buffer:
            with wave.open(wav_buffer, 'wb') as wav:
                # pylint: disable=no-member
                wav.setnchannels(CHANNELS)
                wav.setsampwidth(SAMPLE_WIDTH)
                wav.setframerate(FRAME_RATE)
                wav.writeframes(frames)
            self.mqtt.publish(AUDIO_FRAME.format(self.config.site),
                              wav_buffer.getvalue())

    def send_audio_frames(self):
        """Send the recorded audio frames continuously in AUDIO_FRAME
        messages on MQTT.
        """
        stream = self.audio.open(format=pyaudio.paInt16, channels=CHANNELS,
                                 rate=FRAME_RATE, input=True,
                                 frames_per_buffer=CHUNK)

        print('Started broadcasting audio from device {}'
              ' on site {}'.format(self.audio_in, self.config.site))

        in_speech = False
        silence_frames = int(FRAME_RATE / CHUNK * self.config.vad.silence)

        # TODO: Simplify if ... if ... if ...
        while True:
            frames = stream.read(CHUNK, exception_on_overflow=False)
            if self.config.vad.enabled and self.vad.is_speech(frames, FRAME_RATE):
                if not in_speech:
                    in_speech = True
                    silence_frames = int(FRAME_RATE / CHUNK * self.config.vad.silence)
                    print('Voice activity started on site {}'.format(self.config.site))
                    if self.config.vad.status_messages:
                        self.mqtt.publish(VAD_UP.format(self.config.site),
                                          json.dumps({'siteId': self.config.site,
                                                      'signalMs': 0}))  # Not used
                self.publish_frames(frames)
            elif self.config.vad.enabled:
                if in_speech and silence_frames > 0:
                    self.publish_frames(frames)
                    silence_frames -= 1
                elif in_speech:
                    in_speech = False
                    print('Voice activity stopped on site {}'.format(self.config.site))
                    if self.config.vad.status_messages:
                        self.mqtt.publish(VAD_DOWN.format(self.config.site),
                                          json.dumps({'siteId': self.config.site,
                                                      'signalMs': 0}))  # Not used
            else:
                self.publish_frames(frames)
