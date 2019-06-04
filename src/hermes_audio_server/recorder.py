"""Module with the Hermes audio recorder class."""
import io
import json
from threading import Thread
import wave

import pyaudio
import webrtcvad

from hermes_audio_server.exceptions import NoDefaultAudioDeviceError
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
        self.logger.debug('Probing for available input devices...')
        for index in range(self.audio.get_device_count()):
            device = self.audio.get_device_info_by_index(index)
            name = device['name']
            channels = device['maxInputChannels']
            if channels:
                self.logger.debug('[%d] %s', index, name)
        try:
            self.audio_in = self.audio.get_default_input_device_info()['name']
        except OSError:
            raise NoDefaultAudioDeviceError('input')
        self.logger.info('Connected to audio input %s.', self.audio_in)

        if self.config.vad.enabled:
            self.logger.info('Voice Activity Detection enabled with mode %s.',
                             self.config.vad.mode)
            self.vad = webrtcvad.Vad(self.config.vad.mode)

    def start(self):
        """Start the event loop to the MQTT broker and start the audio
        recording."""
        self.logger.debug('Starting audio thread...')
        Thread(target=self.send_audio_frames, daemon=True).start()
        super().start()

    def publish_frames(self, frames):
        """Publish frames on MQTT."""
        with io.BytesIO() as wav_buffer:
            with wave.open(wav_buffer, 'wb') as wav:
                # pylint: disable=no-member
                wav.setnchannels(CHANNELS)
                wav.setsampwidth(SAMPLE_WIDTH)
                wav.setframerate(FRAME_RATE)
                wav.writeframes(frames)

            audio_frame_topic = AUDIO_FRAME.format(self.config.site)
            audio_frame_message = wav_buffer.getvalue()
            self.mqtt.publish(audio_frame_topic, audio_frame_message)
            self.logger.debug('Published message on MQTT topic:')
            self.logger.debug('Topic: %s', audio_frame_topic)
            self.logger.debug('Message: %d bytes', len(audio_frame_message))

    def publish_vad_status_message(self, message):
        """Publish a status message about the VAD on MQTT."""
        if self.config.vad.status_messages:
            vad_status_topic = message.format(self.config.site)
            vad_status_message = json.dumps({'siteId': self.config.site,
                                             'signalMs': 0})  # Not used
            self.mqtt.publish(vad_status_topic, vad_status_message)
            self.logger.debug('Published message on MQTT topic:')
            self.logger.debug('Topic: %s', vad_status_topic)
            self.logger.debug('Message: %s', vad_status_message)

    def send_audio_frames(self):
        """Send the recorded audio frames continuously in AUDIO_FRAME
        messages on MQTT.
        """
        self.logger.debug('Opening audio input stream...')
        stream = self.audio.open(format=pyaudio.paInt16, channels=CHANNELS,
                                 rate=FRAME_RATE, input=True,
                                 frames_per_buffer=CHUNK)

        self.logger.info('Starting broadcasting audio from device %s'
                         ' on site %s...', self.audio_in, self.config.site)

        in_speech = False
        silence_frames = int(FRAME_RATE / CHUNK * self.config.vad.silence)

        # TODO: Simplify if ... if ...
        while True:
            frames = stream.read(CHUNK, exception_on_overflow=False)
            if self.config.vad.enabled and self.vad.is_speech(frames, FRAME_RATE):
                if not in_speech:
                    in_speech = True
                    silence_frames = int(FRAME_RATE / CHUNK * self.config.vad.silence)
                    self.logger.info('Voice activity started on site %s.',
                                     self.config.site)
                    self.publish_vad_status_message(VAD_UP)
                self.publish_frames(frames)
            elif self.config.vad.enabled:
                if in_speech and silence_frames > 0:
                    self.publish_frames(frames)
                    silence_frames -= 1
                elif in_speech:
                    in_speech = False
                    self.logger.info('Voice activity stopped on site %s.',
                                     self.config.site)
                    self.publish_vad_status_message(VAD_DOWN)
            else:
                self.publish_frames(frames)
