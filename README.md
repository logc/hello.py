hello.py: an example Python package
===================================

# Installation

This is a setuptools package and can be installed with:

    $ python setup.py install

# Usage

After installation, you will find a new executable on your command line that
just prints "Hello world!"

    $ hello
    Hello world!

# Develop

## Setup an environment

If you want to develop the package, it is recommended to create a dedicated
virtualenv and link the package there as a development dependency: 

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ python setup.py develop
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
