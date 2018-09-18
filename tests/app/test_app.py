from flask_philo_core import init_app, init_urls
from flask_philo_core.exceptions import ConfigurationError
from unittest.mock import patch

import os
import pytest
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


@patch.dict(os.environ, {'FLASK_PHILO_SETTINGS_MODULE': 'config.settings'})
def create_app():
    return init_app(__name__, BASE_DIR)


def test_app_creation():
    """
    Test if a Flask-Philo_Core app is created properly
    """

    # check that raises error if not settings file is provided
    with pytest.raises(ConfigurationError):
        init_app(__name__, BASE_DIR)

    with patch.dict(
            os.environ, {'FLASK_PHILO_SETTINGS_MODULE': 'config.settings'}):
        app = create_app()
        assert app is not None
        assert app.name == __name__


def test_init_urls():
    os.environ['FLASK_PHILO_SETTINGS_MODULE'] = 'config.settings'
    app = create_app()
    assert 'URLS' not in app.config

    rules = [r for r in app.url_map.iter_rules()]
    endpoints = [rl.endpoint for rl in rules]
    assert 1 == len(endpoints)
    assert 'static' in endpoints

    with patch.dict(app.config, {'URLS': 'app.urls'}):
        init_urls(app)
        rules2 = [r for r in app.url_map.iter_rules()]
        endpoints2 = [rl.endpoint for rl in rules2]
        assert 3 == len(endpoints2)
        assert 'cors' in endpoints2
        assert 'static' in endpoints2
        assert 'home' in endpoints2
