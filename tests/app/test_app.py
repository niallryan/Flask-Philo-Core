from flask_philo_core import init_app
from flask_philo_core.test import create_test_app
from flask_philo_core.exceptions import ConfigurationError
from unittest.mock import patch

import os
import pytest
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def test_app_creation():
    """
    Test if a Flask-Philo_Core app is created properly
    """

    # check that raises error if not settings file is provided
    with pytest.raises(ConfigurationError):
        init_app(__name__, BASE_DIR)

    with patch.dict(
        os.environ, {
            'FLASK_PHILO_SETTINGS_MODULE': 'config.settings'}):
        app = create_test_app(__name__, BASE_DIR)
        assert app is not None
        assert app.name == __name__
