"""
Module with main entry points for the hello package
"""
import argparse
import sys


def parse_command_line(command_line):
    """
    Defines command line arguments and parses them.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='world')
    return parser.parse_args(command_line)


def compose(name='world'):
    """
    Composes the message that has to be printed.
    """
    return "Hello {0}!".format(name)


def run():
    """
    Main entry point.
    """
    args = parse_command_line(sys.argv[1:])
    message = compose(args.name)
    print message
