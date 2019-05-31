"""This module contains helper functions to log messages from Hermes Audio
Server."""
import logging
from logging.handlers import SysLogHandler
import sys

from hermes_audio_server.exceptions import UnsupportedPlatformError


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
    logger = logging.getLogger(command)
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if daemon:
        handler = SysLogHandler(address=get_domain_socket())
        formatter = logging.Formatter(fmt='{}[%(process)d]: %(message)s'.format(command))
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler(stream=sys.stdout)

    logger.addHandler(handler)
    return logger
