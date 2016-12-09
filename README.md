hello.py: an example Python package
===================================

# Installation

This is a setuptools package and can be installed with:

    $ python setup.py install

A database will be used if a database section is available in the configuration.
Only MySQL is supported as database server at this time. For instructions on how
to install and launch a MySQL server, please see their documentation.

During installation, the MySQL root user password will be requested from you.
This is only ever used to create a new user, `hellouser`, and a new database,
`hellodb`, where data for this package is persisted. A generated password for
this new user is printed; **please note it down** in order to configure
correctly 'hello'.

    $ python setup.py install
    running install
    MySQL root password:
    New password for hellodb user 'hellouser': P9Njvgzsgkfn

You can also set the MySQL root password as an environment variable,
`MYSQLROOTPWD`.

# Usage

After installation, you will find a new executable on your command line that
just prints "Hello world!"

    $ hello
    Hello world!

## Command line arguments

You can also specify a name to be greeted on the command line:

    $ hello --name Brian
    Hello Brian!

You can also specify a configuration file on the command line:

    $ hello --config sample.cfg

If you want to enable logging, set a low integer as the log-level argument.
Refer to `--help` for more details.

    $ hello --log-level 1
    2016-12-03 14:33:51 main.compose DEBUG Composed a greeting: Hello world!
    Hello world!

## Configuration

You can change the greeting message on the configuration file included,
`hello.cfg`. If you edit the `greeting` value to hold someting:

    [general]
    greeting=Good morning

then:

    $ hello
    Good morning world!

### Database configuration

If you want to enable a persistent storage, you have to provide a `[database]`
section in your configuration, with the following settings:

    [database]
    host=
    name=
    user=
    password=

Where `host` is the name of the machine where the database server is located
(default is `localhost`), `name` is the database name (default is `hellodb`),
user is the connection user for this server (default is `hellouser`), and
password is the password that was generated and printed during installation.

You can leave all settings blank, **except for password**. Please include all
setting lines, even if they are blank.

If a database is configured and the corresponding server is running, then the
usage of `hello` will remember how many times it was asked to greet a name:

    $ hello --name John
    Hello John! I have never seen you!

    $ hello --name John
    Hello John! I have seen you 1 times!

    $ hello --name John
    Hello John! I have seen you 2 times!

# Develop

## Setup an environment

If you want to develop the package, it is recommended to create a dedicated
virtualenv and link the package there as a development dependency:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ python setup.py develop
    running develop
    MySQL root password:
    New password for hellodb user 'hellouser': P9Njvgzsgkfn
    ...

The same database initiation is done for 'develop' as for 'install'. Please
refer to the installation section.

    (venv) $ hello
    Hello world!

You will need to install the development dependencies, which are listed in a
separate file `requirements.dev.txt`. These are depependencies that are not
required to use the package. A normal user might not want them; that is why
they are not listed in `setup.py`.

    (venv) $ pip install -r requirements.dev.txt

No `.gitignore` file is included in the repository to avoid assuming which
development tools or styles are you using. It is recommended to ignore at least
the virtual environment:

    $ cat << EOF > .gitignore
    /.gitignore
    venv
    EOF

## Run unit tests

Before and after you change any source code, you should run the unit tests to
check that everything is working.

    (venv) $ python setup.py test
    tests.test_main.test_hello_world
    Checks that the simplest message is 'Hello world!' ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.005s

    OK

# Uninstall

There is no standard way to uninstall setuptools packages. You can either
install `pip` and use:

    $ pip uninstall hello

Or record the installed files and then remove them:

    $ python setup.py install --record files.txt; cat files.txt | xargs rm -rf

# License

MIT License. Copyright (c) 2016 Luis Osa. See LICENSE.txt for further details
