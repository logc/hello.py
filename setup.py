"""
setup script for the hello package
"""
import os
import getpass
import string

from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
import MySQLdb


class DatabaseInstall(install):
    """
    Subclasses the setuptools install command to add database initiation
    """

    def run(self):
        initiate_db()
        install.run(self)


class DatabaseDevelop(develop):
    """
    Subclasses the setuptools develop command to add database initiation
    """

    def run(self):
        initiate_db()
        develop.run(self)


def initiate_db():
    """
    Initiates database so that it can be used by 'hello'. Requests the MySQL
    root password from the user or from the environment.
    """
    root_password = os.getenv('MYSQLROOTPWD') or \
        getpass.getpass("MySQL root password: ")
    hello_password = generate_password()
    print "New password for hellodb user 'hellouser': {0}".format(
        hello_password)
    create_db_user(root_password, hello_password)
    create_db_table(hello_password)


def create_db_user(root_password, hello_password):
    """
    Creates a user in the database and grants minimal privileges to that user
    in order to create a database and create tables within that database.
    """
    conn = MySQLdb.connect(
        host="localhost", user="root", passwd=root_password)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS hellodb;")
    cursor.execute(
        "GRANT USAGE ON *.* TO 'hellouser'@'localhost' "
        "IDENTIFIED BY %(pwd)s;",
        {'pwd': hello_password})
    cursor.execute(
        "GRANT ALL PRIVILEGES ON hellodb.* TO 'hellouser'@'localhost';")
    cursor.close()
    conn.close()


def create_db_table(hello_password):
    """
    Creates a hardcoded table within a database. The passed in password must
    have enought privileges to create tables.
    """
    conn = MySQLdb.connect(
        host="localhost", user="hellouser", passwd=hello_password,
        db="hellodb")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS greeted ("
        "  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        "  name VARCHAR(100), "
        "  counter INT NOT NULL DEFAULT 1, "
        "  INDEX(name(10))"
        ");")
    cursor.close()
    conn.close()


def generate_password():
    """
    Generates a random password of fixed length.

    See:
    http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
    """
    chars = string.letters + string.digits + '$!'
    return ''.join([chars[ord(os.urandom(1)) % len(chars)] for _ in xrange(12)])


setup(name='hello.py',
      version='0.1.0',
      packages=['hello'],
      test_suite='nose.collector',
      install_requires=['mysql'],
      entry_points={
          'console_scripts': [
              'hello = hello.main:run']},
      cmdclass={
          'install': DatabaseInstall,
          'develop': DatabaseDevelop})
