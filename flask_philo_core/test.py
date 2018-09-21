from flask_philo_core import init_app
from decimal import Decimal
from unittest.mock import patch

import flask
import os
import random
import string
import uuid

def create_test_app(
        name, base_dir, config_module='config.settings', config_dict={}):
    patch(config_module, config_dict)

    with patch.dict(
        os.environ, {'FLASK_PHILO_SETTINGS_MODULE': config_module}):
        app = init_app(name, base_dir)
        return app

class FlaskPhiloTestCase(object):
    """
    This tests should be used when testing views
    """

    def setup(self):
        self.mock_config = {}
    
        self.app = create_test_app()



        self.client = self.app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def update_urls(self):
        init_urls(self.app)



class BaseTestFactory(object):
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
