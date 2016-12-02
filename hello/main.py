"""
Module with main entry points for the hello package
"""


def compose():
    """
    Composes the message that has to be printed.
    """
    return "Hello world!"


def run():
    """
    Main entry point.
    """
    message = compose()
    print message
