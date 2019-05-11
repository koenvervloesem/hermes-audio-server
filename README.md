# Hermes Audio Server

[![Build status](https://api.travis-ci.com/koenvervloesem/hermes-audio-server.svg?branch=master)](https://travis-ci.com/koenvervloesem/hermes-audio-server) [![Maintainability](https://api.codeclimate.com/v1/badges/9ae3a46a15a85c8b44f3/maintainability)](https://codeclimate.com/github/koenvervloesem/hermes-audio-server/maintainability) [![Code quality](https://api.codacy.com/project/badge/Grade/02647c1d9d214b8a97ed124ccf48839f)](https://www.codacy.com/app/koenvervloesem/hermes-audio-server) [![Python versions](https://img.shields.io/badge/python-3.5|3.6|3.7-blue.svg)](https://www.python.org) [![GitHub license](https://img.shields.io/github/license/koenvervloesem/hermes-audio-server.svg)](https://github.com/koenvervloesem/hermes-audio-server/blob/master/LICENSE)

Hermes Audio server implements the audio server part of the [Hermes protocol](https://docs.snips.ai/reference/hermes) defined by [Snips](http://snips.ai).

It's meant to be used with [Rhasspy](https://rhasspy.readthedocs.io), an offline, multilingual voice assistant toolkit that works with [Home Assistant](https://www.home-assistant.io) and is completely open source.

With Hermes Audio Server, you can use the microphone and speaker of your computer (such as a Raspberry Pi) as remote audio input and output for a Rhasspy system.

## System requirements

Hermes Audio Server requires Python 3. It has been tested on a Raspberry Pi running Raspbian 9.8, but in principle it should be cross-platform. Please open an issue on GitHub when you encounter problems on your platform.

## Installation

You can install the dependencies like this:

```shell
sudo apt install portaudio19-dev
pip3 install hermes-audio-server 
```

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
    }
}
```

All keys are optional. The default behaviour is to connect with `localhost:1883` without authentication and TLS and to use `default` as the site ID.

Currently Hermes Audio Server uses the system's default microphone and speaker. In the next version this will be configurable.

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

## TODO list

The following features will be developed soon:

*   Add logging
*   Make it possible to run the commands as daemons (and add systemd unit files)
*   Add an option to let the user choose the audio devices
*   Add more documentation

## Other interesting projects

If you find Hermes Audio Server interesting, also have a look at the following projects:

*   [Rhasspy](https://rhasspy.readthedocs.io): An offline, multilingual voice assistant toolkit that works with [Home Assistant](https://www.home-assistant.io) and is completely open source.
*   [Snips Led Control](https://github.com/Psychokiller1888/snipsLedControl): An easy way to control the leds of your Snips-compatible device, with led patterns when the hotword is detected, the device is listening, speaking, idle, ...
*   [Matrix-Voice-ESP32-MQTT-Audio-Streamer](https://github.com/Romkabouter/Matrix-Voice-ESP32-MQTT-Audio-Streamer): The equivalent of Hermes Audio Server for a Matrix Voice ESP32 board, including LED control and OTA updates.
*   [OpenSnips](https://github.com/syntithenai/opensnips): A collection of open source projects related to the Snips voice platform.

## License

This project is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software with the MIT license. See the LICENSE file for more information.
