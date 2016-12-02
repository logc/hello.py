"""
test module for the main module
"""
import shlex

from nose.tools import assert_equal

import hello.main


def test_hello_world():
    """
    Checks that the simplest message is 'Hello world!'
    """
    expected = "Hello world!"
    actual = hello.main.compose()
    assert_equal(actual, expected)


def test_hello_name():
    """
    Checks that a name can be specified for the greeting
    """
    name = "Guido"
    expected = "Hello Guido!"
    actual = hello.main.compose(name)
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
