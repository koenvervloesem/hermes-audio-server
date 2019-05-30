# Hermes Audio Server

[![Build status](https://api.travis-ci.com/koenvervloesem/hermes-audio-server.svg?branch=master)](https://travis-ci.com/koenvervloesem/hermes-audio-server) [![Maintainability](https://api.codeclimate.com/v1/badges/9ae3a46a15a85c8b44f3/maintainability)](https://codeclimate.com/github/koenvervloesem/hermes-audio-server/maintainability) [![Code quality](https://api.codacy.com/project/badge/Grade/02647c1d9d214b8a97ed124ccf48839f)](https://www.codacy.com/app/koenvervloesem/hermes-audio-server) [![Python versions](https://img.shields.io/badge/python-3.5|3.6|3.7-blue.svg)](https://www.python.org) [![PyPI package version](https://img.shields.io/pypi/v/hermes-audio-server.svg)](https://pypi.python.org/pypi/hermes-audio-server) [![GitHub license](https://img.shields.io/github/license/koenvervloesem/hermes-audio-server.svg)](https://github.com/koenvervloesem/hermes-audio-server/blob/master/LICENSE)

Hermes Audio server implements the audio server part of the [Hermes protocol](https://docs.snips.ai/reference/hermes) defined by [Snips](http://snips.ai).

It's meant to be used with [Rhasspy](https://rhasspy.readthedocs.io), an offline, multilingual voice assistant toolkit that works with [Home Assistant](https://www.home-assistant.io) and is completely open source.

With Hermes Audio Server, you can use the microphone and speaker of your computer (such as a Raspberry Pi) as remote audio input and output for a Rhasspy system.

## System requirements

Hermes Audio Server requires Python 3. It has been tested on a Raspberry Pi running Raspbian 9.8, but in principle it should be cross-platform. Please open an issue on GitHub when you encounter problems on your platform.

## Installation

You can install Hermes Audio Server and its dependencies like this:

```shell
sudo apt install portaudio19-dev
sudo pip3 install hermes-audio-server
```

Note: this installs Hermes Audio Server globally. If you want to install Hermes Audio Server in a Python virtual environment, drop the `sudo`.

## Configuration

Hermes Audio Server is configured in the JSON file `/etc/hermes-audio-server.json`, which has the following format:

```json
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
    },
    "vad": {
        "mode": 0,
        "silence": 2,
        "status_messages": true
    }
}
```

All keys are optional. The default behaviour is to connect with `localhost:1883` without authentication and TLS and to use `default` as the site ID.

Currently Hermes Audio Server uses the system's default microphone and speaker. In the next version this will be configurable.

### Voice Activity Detection
Voice Activity Detection is an experimental feature in Hermes Audio Server, which is disabled by default. It is based on [py-webrtcvad](https://github.com/wiseman/py-webrtcvad) and tries to suppress sending audio frames when there's no speech. Note that the success of this attempt highly depends on your microphone, your environment and your configuration of the VAD feature. Voice Activity Detection in Hermes Audio Server should not be considered a privacy feature, but a feature to save network bandwidth. If you really don't want to send audio frames on your network except when giving voice commands, you should run a wake word service on your device and only then start streaming audio to your Rhasspy server until the end of the command.

If the `vad` key is not specified in the configuration file, Voice Activity Detection is not enabled and all recorded audio frames are streamed continuously on the network. If you don't want this, specify the `vad` key to only stream audio when voice activity is detected. You can configure the VAD feature with the following subkeys:

*   `mode`: This should be an integer between 0 and 3. 0 is the least aggressive about filtering out non-speech, 3 is the most aggressive. Defaults to 0.
*   `silence`: This defines how much silence (no speech detected) in seconds has to go by before Hermes Audio Recorder considers it the end of a voice message. Defaults to 2. Make sure that this value is higher than or equal to `min_sec` [in the configuration of WebRTCVAD](https://rhasspy.readthedocs.io/en/latest/command-listener/#webrtcvad) for the command listener of Rhasspy, otherwise the audio stream for the command listener could be aborted too soon.
*   `status_messages`: This is a boolean: `true` or `false`. Specifies whether or not Hermes Audio Recorder sends messages on MQTT when it detects the start or end of a voice message. Defaults to `false`. This is useful for debugging, when you want to find the right values for `mode` and `silence`.

## Running Hermes Audio Server

Hermes Audio Server consists of two commands: Hermes Audio Player that receives WAV files on MQTT and plays them on the speaker, and Hermes Audio Recorder that records WAV files from the microphone and sends them as audio frames on MQTT.

You can run the Hermes Audio Player like this:

```shell
hermes-audio-player
```

You can run the Hermes Audio Recorder like this:

```shell
hermes-audio-recorder
```

You can run both, or only one of them if you only want to use the speaker or microphone.

## Usage

Both commands know the `--help` option that gives you more information about the recognized options. For instance:

```shell
usage: hermes-audio-player [-h] [-v] [-V] [-c CONFIG]

hermes-audio-player is an audio server implementing the playback part of
    the Hermes protocol.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         use verbose output
  -V, --version         print version information and exit
  -c CONFIG, --config CONFIG
                        configuration file [default: /etc/hermes-audio-
                        server.json]
```

## Known issues / TODO list

*   There's no logging yet, although the commands show what they are doing on stdout.
*   The commands don't have a daemon mode yet.
*   You can't choose the audio devices yet: the commands use the system's default microphone and speaker.
*   This project is really a minimal implementation of the audio server part of the Hermes protocol, meant to be used with Rhasspy. It's not a drop-in replacement for snips-audio-server, as it lacks [additional metadata](https://github.com/snipsco/snips-issues/issues/144#issuecomment-494054082) in the WAV frames.

## Changelog

*   0.1.1 (2019-05-30): Made the audio player more robust when receiving an incorrect WAV file.
*   0.1.0 (2019-05-16): Added Voice Activity Detection option.
*   0.0.2 (2019-05-11): First public version.

## Other interesting projects

If you find Hermes Audio Server interesting, also have a look at the following projects:

*   [Rhasspy](https://rhasspy.readthedocs.io): An offline, multilingual voice assistant toolkit that works with [Home Assistant](https://www.home-assistant.io) and is completely open source.
*   [Snips Led Control](https://github.com/Psychokiller1888/snipsLedControl): An easy way to control the leds of your Snips-compatible device, with led patterns when the hotword is detected, the device is listening, speaking, idle, ...
*   [Matrix-Voice-ESP32-MQTT-Audio-Streamer](https://github.com/Romkabouter/Matrix-Voice-ESP32-MQTT-Audio-Streamer): The equivalent of Hermes Audio Server for a Matrix Voice ESP32 board, including LED control and OTA updates.
*   [OpenSnips](https://github.com/syntithenai/opensnips): A collection of open source projects related to the Snips voice platform.

## License

This project is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software with the MIT license. See the LICENSE file for more information.
