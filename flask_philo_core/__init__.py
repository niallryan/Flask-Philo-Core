from flask import Flask

from . import default_settings
from .exceptions import ConfigurationError
from .logger import init_logging
from flask_cors import CORS
import importlib
import os



def init_app(module, BASE_DIR, **kwargs):
    """
    Initalize an app, call this method once from start_app
    Implements Application Factory concept described at
    http://flask.pocoo.org/docs/1.0/patterns/appfactories/#app-factories
    """

    def init_config(app):
        """
        Load settings module and attach values to the application
        config dictionary
        """
        if 'FLASK_PHILO_SETTINGS_MODULE' not in os.environ:
            raise ConfigurationError('No settings has been defined')

        app.config['BASE_DIR'] = BASE_DIR

        # Flask-Philo-Core default configuration values are
        # appended to the app configuration
        for v in dir(default_settings):
            app.config[v] = getattr(default_settings, v)

        # Append configuration defined in settings file to the app
        settings = importlib.import_module(
            os.environ['FLASK_PHILO_SETTINGS_MODULE'])

        for v in dir(settings):
            app.config[v] = getattr(settings, v)

        def init_urls():
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
                CORS(app, resources=app.config['CORS'])


        init_logging(app)
        init_urls()
        init_cors(app)

    app = Flask(module)
    init_config(app)
    return app
