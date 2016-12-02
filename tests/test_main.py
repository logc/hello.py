"""
test module for the main module
"""
from nose.tools import assert_equal

import hello.main


def test_hello_world():
    """
    Checks that the simplest message is 'Hello world!'
    """
    expected = "Hello world!"
    actual = hello.main.compose()
    assert_equal(actual, expected)
