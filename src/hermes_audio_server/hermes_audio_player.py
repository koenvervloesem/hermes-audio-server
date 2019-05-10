import plac

from __about__ import __player__
import cli
from config import DEFAULT_CONFIG


def main(verbose: ('use verbose output', 'flag', 'v'),
         version: ('print version information and exit', 'flag', 'V'),
         config: ('configuration file [default: {}]'.format(DEFAULT_CONFIG),
                  'option', 'c')):
    """hermes-audio-player is an audio server implementing the playback part of
    the Hermes protocol."""
    cli.main(__player__, verbose, version, config)


if __name__ == '__main__':
    plac.call(main)
