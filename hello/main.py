"""
Module with main entry points for the hello package
"""
import argparse
import sys
import ConfigParser
import logging

import MySQLdb
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


def comment_if_already_seen(greeted_name, config):
    """
    Checks in a persistent storage if we have already greeted the given name,
    and returns a string where the number of times we have greeted that name is
    mentioned.
    """
    credentials = get_database_credentials(config)
    if not credentials:
        return ""
    host, name, user, password = credentials
    comment = " "
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=password, db=name)
        cursor = conn.cursor()
        cursor.execute("SELECT counter FROM greeted WHERE name = %(name)s",
                       {'name': greeted_name})
        row = cursor.fetchone()
        if row is None:
            comment += "I have never seen you!"
            cursor.execute("INSERT INTO greeted(name) VALUES (%(name)s)",
                           {'name': greeted_name})
        else:
            counter = row[0]
            comment += "I have seen you {0} times!".format(counter)
            cursor.execute(
                "UPDATE greeted SET counter=%(counter)s WHERE name=%(name)s",
                {'name': greeted_name, 'counter': counter + 1})
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.OperationalError as err:
        logging.error(str(err))
    return comment


def get_database_credentials(config):
    try:
        host = config.get('database', 'host') or 'localhost'
        name = config.get('database', 'name') or 'hellodb'
        user = config.get('database', 'user') or 'hellouser'
        password = config.get('database', 'password')
        if not password:
            logging.error('No password configured for database %s and user %s',
                          name, user)
        else:
            return host, name, user, password
    except ConfigParser.NoSectionError:
        logging.info("No database configuration found; no persistent results")
    except ConfigParser.NoOptionError as ex:
        logging.error("Config section 'database' does not have option '%s'",
                      ex.option)


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
    message += comment_if_already_seen(args.name, config)
    print message
