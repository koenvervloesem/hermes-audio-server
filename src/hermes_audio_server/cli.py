"""This module contains the main function run by the CLI commands
hermes-audio-player and hermes-audio-recorder.
"""
from json import JSONDecodeError
import signal
import sys

from daemon import DaemonContext

from hermes_audio_server.about import VERSION
from hermes_audio_server.config import ServerConfig, DEFAULT_CONFIG
from hermes_audio_server.exceptions import ConfigurationFileNotFoundError, \
    UnsupportedPlatformError
from hermes_audio_server.logger import get_logger
from hermes_audio_server.player import AudioPlayer
from hermes_audio_server.recorder import AudioRecorder

SERVER = {'hermes-audio-player': AudioPlayer,
          'hermes-audio-recorder': AudioRecorder}


def main(command, verbose, version, config, daemon):
    """The main function run by the CLI command.

    Args:
        command (str): The command to run.
        verbose (bool): Use verbose output if True.
        version (bool): Print version information and exit if True.
        config (str): Configuration file.
        daemon (bool): Run as a daemon if True.
    """
    # Define signal handlers to cleanly exit the program.
    def quit_process(signal_number, frame):
        print('Received SIGQUIT signal')
        server.stop()
        sys.exit(0)

    def terminate_process(signal_number, frame):
        print('Received SIGTERM signal')
        server.stop()
        sys.exit(0)

    # Register signals
    signal.signal(signal.SIGQUIT, quit_process)
    signal.signal(signal.SIGTERM, terminate_process)

    try:

        logger = get_logger(command, verbose, daemon)
        logger.info('%s %s', command, VERSION)

        # Daemonize the program
        if daemon:
            context = DaemonContext(files_preserve=[logger.handlers[0].socket])
            context.signal_map = {signal.SIGQUIT: quit_process,
                                  signal.SIGTERM: terminate_process}
            context.open()

        if not version:
            if not config:
                config = DEFAULT_CONFIG

            server = SERVER[command](ServerConfig.from_json_file(config),
                                     verbose, logger)

            server.start()
    except ConfigurationFileNotFoundError as error:
        logger.critical('Configuration file %s not found. Exiting...', error.filename)
        sys.exit(1)
    except JSONDecodeError as error:
        logger.critical('%s is not a valid JSON file. Parsing failed at line %s and column %s. Exiting...', config, error.lineno, error.colno)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('Received SIGINT signal. Shutting down %s...', command)
        server.stop()
        sys.exit(0)
    except PermissionError as error:
        logger.critical('Can\'t read file %s. Make sure you have read permissions. Exiting...', error.filename)
        sys.exit(1)
    except UnsupportedPlatformError as error:
        print('Error: {} is not a supported platform.'.format(error.platform))
        sys.exit(1)
