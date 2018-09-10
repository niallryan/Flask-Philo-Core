from flask import Flask

from . import default_settings
from .exceptions import ConfigurationError
from .logger import init_logging

import importlib
import os


def init_urls(app):
    if 'URLS' in app.config:
        # Read urls from file and bind routes and views
        urls_module = importlib.import_module(app.config['URLS'])
        for route in urls_module.URLS:
            app.add_url_rule(
                route[0], view_func=route[1].as_view(route[2]))


def init_cors(app):
    """
    Initializes cors protection if config
    """
    if 'CORS' in app.config:
        from flask_cors import CORS
        CORS(app, resources=app.config['CORS'])


def init_config(app, base_dir):
    """
    Load settings module and attach values to the application
    config dictionary
    """
    if 'FLASK_PHILO_SETTINGS_MODULE' not in os.environ:
        raise ConfigurationError('No settings has been defined')

    app.config['base_dir'] = base_dir

    # Flask-Philo-Core default configuration values are
    # appended to the app configuration
    for v in dir(default_settings):
        app.config[v] = getattr(default_settings, v)

    # Append configuration defined in settings file to the app
    settings = importlib.import_module(
        os.environ['FLASK_PHILO_SETTINGS_MODULE'])

    for v in dir(settings):
        app.config[v] = getattr(settings, v)



def init_app(module, base_dir):
    """
    Initalize an app, call this method once from start_app
    Implements Application Factory concept described at
    http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
    """
    app = Flask(module)
    init_config(app, base_dir)
    init_logging(app)
    init_urls(app)
    init_cors(app)
    return app
