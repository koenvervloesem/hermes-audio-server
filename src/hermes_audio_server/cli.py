"""This module contains the main function run by the CLI commands
hermes-audio-player and hermes-audio-recorder.
"""
from hermes_audio_server.about import VERSION
from hermes_audio_server.config import ServerConfig, DEFAULT_CONFIG
from hermes_audio_server.player import AudioPlayer
from hermes_audio_server.recorder import AudioRecorder

SERVER = {'hermes-audio-player': AudioPlayer,
          'hermes-audio-recorder': AudioRecorder}


def main(command, verbose, version, config):
    """The main function run by the CLI command.

    Args:
        command (str): The command to run.
        verbose (bool): Use verbose output or not.
        version (bool): Print version information and exit.
        config (str): Configuration file.
    """
    print('{} {}'.format(command, VERSION))
    try:
        if not version:
            if not config:
                config = DEFAULT_CONFIG

            server = SERVER[command](ServerConfig.from_json_file(config),
                                     verbose)

            server.start()
    except FileNotFoundError as not_found:
        print('Configuration file {}.'.format(not_found))
    except KeyboardInterrupt:
        print('Shutting down {}...'.format(command))
        server.audio.terminate()
