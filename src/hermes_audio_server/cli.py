"""This module contains the main function run by the CLI commands
hermes-audio-player and hermes-audio-recorder.
"""
import sys
import traceback

from hermes_audio_server.__about__ import __version__
from hermes_audio_server.config import ServerConfig, DEFAULT_CONFIG
from hermes_audio_server.player import AudioPlayer
from hermes_audio_server.recorder import AudioRecorder


def main(command, verbose, version, config):
    """The main function run by the CLI command.

    Args:
        command (str): The command to run.
        verbose (bool): Use verbose output or not.
        version (bool): Print version information and exit.
        config (str): Configuration file.
    """
    try:
        print('{} {}'.format(command, __version__))
        if not version:
            if not config:
                config = DEFAULT_CONFIG

            if command == 'hermes-audio-player':
                server = AudioPlayer(ServerConfig.from_json_file(config),
                                     verbose)
            elif command == 'hermes-audio-recorder':
                server = AudioRecorder(ServerConfig.from_json_file(config),
                                       verbose)

            server.start()
    except FileNotFoundError as not_found:
        print('Configuration file {}.'.format(not_found))
    except KeyboardInterrupt:
        print('Shutting down {}...'.format(command))
        server.audio.terminate()
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
