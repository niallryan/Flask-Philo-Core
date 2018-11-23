Console Commands
=============================================

Flask-Philo_Core provides console commands to manage core app services and common tasks (e.g. ``runserver``, ``test``, etc).

However, Flask-Philo-Core also allows us to *extend* this set of console commands with our own *custom* commands.
This let us write custom utilities and tools that take advantage of the inherent features of a Flask-Philo-Core application.

Running Console Commands
----------------------------

In general, we use the ``flask-philo`` command as our starting point for launching console commands. The following
commands are already included as part of Flask-Philo-Core:

::

    $ flask-philo runserver
    $ flask-philo test


Writing Custom Console Commands
--------------------------------------

We can extend our application's set of utility commands by adding Python programs to the ``src/commands`` directory. For example,
when create a file ``src/commands/hello.py`` withe the following source code:

``src/commands/hello.py``
::

    from flask import current_app


    def run():
        app = current_app._get_current_object()
        print('hello')
        print(app)


Once this simple program is saved to the ``src/commands`` directory, it can be run as follows:

::

    $ flask-philo hello
