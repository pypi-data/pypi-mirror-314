import logging
import argparse
import importlib.resources

from modules import starter, execute

with importlib.resources.path('config', 'config.ini') as config_file_path:

    import configparser

    config = configparser.ConfigParser()
    config.read(config_file_path)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

log = logging.getLogger()


def main():
    """
    Main function to parse command-line arguments and execute the necessary actions.

    This function performs the following steps:
    1. Reads the configuration file ('config.ini') to obtain the version and author information.
    2. Displays a banner with the version number.
    3. Initializes an argument parser with the following options:
        - A positional argument 'source' for specifying the path of the source file to analyze.
        - A '-c/--config' flag to access the initial configuration menu.
        - A '-v/--verbose' flag to enable verbose logging mode (debugging).
    4. Based on the arguments provided, it either:
        - Runs the `starter` function if the configuration flag is set.
        - Executes the `execute` function with the provided source path if specified.
        - Displays a help message if no arguments are provided.

    Args:
        None

    Returns:
        None
    """

    version = config['DEFAULT']['version']
    author = config['DEFAULT']['author']
    config_file = config['DEFAULT']['config_file']
    output_file = config['DEFAULT']['output_file']

    banner = f" v{version}     __\n  __ _  ___/ /__  _______\n /  ' \/ _  / _ \/ __(_-<\n/_/_/_/\_,_/\___/\__/___/\n"

    parser = argparse.ArgumentParser(
        prog='mdocs',
        description='Allows to extract docstrings from Python functions to create a documentation file in Markdown format.',
        epilog=f'Thanks for using it. {author}'
    )

    parser.add_argument("source", nargs='?', type=str,
                        help='path of the sorce to analyze')

    parser.add_argument('-c', '--config',  action='store_true',
                        help='initial configuration menu')

    parser.add_argument('-v', '--verbose',  action='store_true',
                        help='run as debug')

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    if args.config:
        print(banner)
        starter(config_file)

    elif args.source:
        execute(args.source, config_file, output_file)

    else:
        print(banner)
        parser.print_help()


if __name__ == "__main__":

    main()
