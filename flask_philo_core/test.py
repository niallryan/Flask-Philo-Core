from flask_philo_core import init_app, init_urls
from decimal import Decimal
from unittest.mock import Mock, patch

import os
import random
import string
import sys
import uuid


def create_test_app(name, base_dir):
    app = init_app(name, base_dir)
    return app


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class FlaskPhiloTestCase(object):
    """
    This tests should be used when testing views
    """
    json_request_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def update_urls(self):
        init_urls(self.app)


class BaseTestFactory(object):
    @classmethod
    def create_test_app(cls, config=None, urls=None):
        config_mock = Mock()
        sys_modules_mock = {}

        if config is not None:
            for k, v in config.items():
                setattr(config_mock, k, v)

        if urls is not None:
            config_mock.URLS = 'app.urls'
            url_mock = Mock()
            url_mock.URLS = urls
            sys_modules_mock['app.urls'] = url_mock

        sys_modules_mock['config.settings'] = config_mock
        with patch.dict(sys.modules, sys_modules_mock):
            with patch.dict(
                os.environ, {
                    'FLASK_PHILO_SETTINGS_MODULE': 'config.settings'}):
                return create_test_app(__name__, BASE_DIR)

    @classmethod
    def create_uuid(cls):
        return uuid.uuid4()

    @classmethod
    def create_unique_string(cls, prefix=None, n_range=20):
        st = ''.join(
            random.choice(
                string.ascii_lowercase + string.digits)
            for x in range(n_range))

        if prefix:
            return '{0}-{1}'.format(prefix, st)
        else:
            return '{0}'.format(st)

    @classmethod
    def create_unique_email(cls):
        return '{0}@{1}.com'.format(
            cls.create_unique_string(), cls.create_unique_string())

    @classmethod
    def create_random_decimal(cls, n=10000):
        return Decimal((random.randrange(n)/100))
