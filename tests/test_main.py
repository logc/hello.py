"""
test module for the main module
"""
import shlex
import StringIO
import textwrap

from nose.tools import assert_equal
from mock import patch

import hello.main


def test_compose():
    """
    Checks how to compose the simplest message
    """
    expected = "Hello world!"
    actual = hello.main.compose('Hello', 'world')
    assert_equal(actual, expected)


def test_parse_command_line():
    """
    Check that a 'name' arg is parsed from command line
    """
    command_line = shlex.split('--name Terry')
    args = hello.main.parse_command_line(command_line)
    expected = 'Terry'
    actual = args.name
    assert_equal(actual, expected)


def test_read_config():
    """
    Checks that a configuration is read
    """
    mock_config_file = StringIO.StringIO()
    mock_config_file.write(textwrap.dedent(
        """
        [general]
        greeting=Good morning
        """))
    mock_config_file.seek(0)
    config = hello.main.read_config(mock_config_file)
    assert_equal('Good morning', config.get('general', 'greeting'))


@patch('hello.main.logging')
def test_logging(mock_logging):
    """
    Checks that a statement is logged
    """
    hello.main.compose('Hi', 'beautiful')
    mock_logging.debug.assert_called_once_with(
        'Composed a greeting: %s', 'Hi beautiful!')
