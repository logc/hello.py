"""
test module for the main module
"""
import shlex
import StringIO
import textwrap

from nose.tools import assert_equal
from mock import patch, MagicMock

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


@patch('MySQLdb.connect')
def test_database_persistence(mock_connect):
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    # Discard reads and writes to database
    mock_cursor.execute_return_value = None
    # Returns None the first time it is called, then 1, then 2 ...
    mock_cursor.fetchone.side_effect = [None, (1,), (2,)]
    mock_config_file = StringIO.StringIO()
    mock_config_file.write(textwrap.dedent(
        """
        [general]
        greeting=

        [database]
        host=
        name=
        user=
        password=password_cannot_be_empty
        """))
    mock_config_file.seek(0)
    config = hello.main.read_config(mock_config_file)
    greeted_name = "Luis"
    expected = " I have never seen you!"
    actual = hello.main.comment_if_already_seen(greeted_name, config)
    assert_equal(actual, expected)

    expected = " I have seen you 1 times!"
    actual = hello.main.comment_if_already_seen(greeted_name, config)
    assert_equal(actual, expected)
