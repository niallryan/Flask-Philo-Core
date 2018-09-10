from flask_philo_core import init_app
from flask_philo_core.exceptions import ConfigurationError
from unittest.mock import MagicMock


import os
import pytest
#import mock
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))

def create_app():
    os.environ['FLASK_PHILO_SETTINGS_MODULE'] = 'config.settings'
    return init_app(__name__, BASE_DIR)



def test_app_creation():
    """
    Test if a Flask-Philo_Core app is created properly
    """

    # check that raises error if not settings file is provided
    with pytest.raises(ConfigurationError):
        init_app(__name__, BASE_DIR)

    os.environ['FLASK_PHILO_SETTINGS_MODULE'] = 'config.settings'

    app = create_app()
    assert app is not None
    assert app.name == __name__
