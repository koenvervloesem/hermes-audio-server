# Hermes Audio Server

Hermes Audio server implements the audio server part of the [Hermes protocol](https://docs.snips.ai/reference/hermes) defined by [Snips](http://snips.ai).

It's meant to be used with [Rhasspy](https://rhasspy.readthedocs.io/en/latest/), an offline, multilingual voice assistant toolkit that works with [Home Assistant](https://www.home-assistant.io/) and is completely open source.

With Hermes Audio Server, you can use the microphone and speaker of your computer (such as a Raspberry Pi) as remote audio input and output for a Rhasspy system.

## System requirements

Hermes Audio Server requires Python 3. It has been tested on a Raspberry Pi running Raspbian 9.8, but in principle it should be cross-platform. Please open an issue on GitHub when you encounter problems on your platform.

## Installation

You can install the dependencies like this:

```shell
sudo apt install portaudio19-dev
pip3 install -r requirements.txt
```

There's currently no installation script for Hermes Audio Server yet. This will be added in the next version.

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

All keys are optional. The default behaviour is to connect with localhost:1883 without authentication and TLS and to use default as the site ID.

Currently Hermes Audio Server uses the system's default microphone and speaker. In the next version this will be configurable.

## Running Hermes Audio Server

Hermes Audio Server consists of two commands: Hermes Audio Player that receives WAV files on MQTT and plays them on the speaker, and Hermes Audio Recorder that records WAV files from the microphone and sends them as audio frames on MQTT.

You can run the Hermes Audio Player like this:

```
python3 src/hermes_audio_server/hermes_audio_player.py
```

You can run the Hermes Audio Recorder like this:

```
python3 src/hermes_audio_server/hermes_audio_recorder.py
```

You can run both, or only one of them if you only want to use the speaker or microphone.

Both commands know the `--help` option that gives you more information about the recognized options.

## TODO

 *   Create installer
 *   Add systemd unit files
 *   Add logging
 *   Option to let the user choose the audio devices
 *   Add documentation

## LICENSE

This project is provided by [Koen Vervloesem](mailto:koen@vervloesem.eu) as open source software with the MIT license. See the LICENSE file for more information.
