import plac

from __about__ import __recorder__
import cli
from config import DEFAULT_CONFIG


def main(verbose: ('use verbose output', 'flag', 'v'),
         version: ('print version information and exit', 'flag', 'V'),
         config: ('configuration file [default: {}]'.format(DEFAULT_CONFIG),
                  'option', 'c')):
    """hermes-audio-recorder is an audio server implementing the recording part
    of the Hermes protocol."""
    cli.main(__recorder__, verbose, version, config)


if __name__ == '__main__':
    plac.call(main)
