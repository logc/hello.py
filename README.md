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

A `.gitignore` file is not included in the repository in order to minimize
assumptions on development tools or styles. It is recommended to ignore at
least the virtual environment:

    $ cat << EOF > .gitignore
    /.gitignore
    venv
    EOF

# Uninstall

There is no standard way to uninstall setuptools packages. You can either
install `pip` and use:

    $ pip uninstall hello

Or record the installed files and then remove them:

    $ python setup.py install --record files.txt; cat files.txt | xargs rm -rf

# License

MIT License. Copyright (c) 2016 Luis Osa. See LICENSE.txt for further details
