"""This module contains helper functions to log messages from Hermes Audio
Server."""
import logging
from logging.handlers import SysLogHandler
import sys

import colorlog

from hermes_audio_server.exceptions import UnsupportedPlatformError

DAEMON_FORMAT = '{}[%(process)d]: %(message)s'
INTERACTIVE_FORMAT = '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(message)s'
LOG_COLORS = {'DEBUG':    'white',
              'INFO':     'green',
              'WARNING':  'yellow',
              'ERROR':    'red',
              'CRITICAL': 'bold_red'}


def get_domain_socket():
    """Get the default domain socket for syslog on this platform."""
    if sys.platform.startswith('linux'):  # Linux
        return '/dev/log'
    if sys.platform.startswith('darwin'):  # macOS
        return '/var/run/syslog'
    # Unsupported platform
    raise UnsupportedPlatformError(sys.platform)


def get_logger(command, verbose, daemon):
    """Return a Logger object with the right level, formatter and handler."""

    if daemon:
        handler = SysLogHandler(address=get_domain_socket())
        formatter = logging.Formatter(fmt=DAEMON_FORMAT.format(command))
        logger = logging.getLogger(command)
    else:
        handler = colorlog.StreamHandler(stream=sys.stdout)
        formatter = colorlog.ColoredFormatter(INTERACTIVE_FORMAT,
                                              log_colors=LOG_COLORS)
        logger = colorlog.getLogger(command)

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
