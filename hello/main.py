"""
Module with main entry points for the hello package
"""
import argparse
import sys
import ConfigParser
import logging

from pkg_resources import Requirement, resource_filename


def parse_config(filename):
    """
    Parses a configuration object from a given file name
    """
    filepath = resource_filename(Requirement.parse("hello.py"), filename)
    with open(filepath, 'r') as config_file:
        config = read_config(config_file)
    return config


def read_config(config_file):
    """
    Reads a configuration object from an opened file handle
    """
    defaults = {'greeting': 'Hello'}
    config = ConfigParser.ConfigParser(defaults, allow_no_value=True)
    config.readfp(config_file)
    return config


def parse_command_line(command_line):
    """
    Defines command line arguments and parses them.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='world')
    parser.add_argument('-c', '--config', default='hello.cfg')
    parser.add_argument(
        '-l', '--log-level', metavar='LEVEL',
        action='store', dest='log_level', default=21,
        type=int, choices=xrange(51),
        help='1 DEBUG; 11 INFO; 21 WARNING; 31 ERROR; 41 CRITICAL')
    return parser.parse_args(command_line)


def compose(greeting, name):
    """
    Composes the message that has to be printed.
    """
    message = "{0} {1}!".format(greeting, name)
    logging.debug('Composed a greeting: %s', message)
    return message


def run():
    """
    Main entry point.
    """
    args = parse_command_line(sys.argv[1:])
    logging.basicConfig(
        format='%(asctime)s %(module)s.%(funcName)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=args.log_level)
    config = parse_config(args.config)
    greeting = config.get('general', 'greeting') or \
        config.defaults().get('greeting')
    message = compose(greeting, args.name)
    print message
