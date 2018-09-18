from decimal import Decimal

import flask
import uuid
import random
import string
#from flask_philo import app
#from flask_philo.db.postgresql.orm import BaseModel
#from flask_philo.db.postgresql import syncdb
#from flask_philo.db.postgresql.connection import get_pool
#from flask_philo.db.redis.connection import get_pool as get_redis_pool
#from flask_philo.db.elasticsearch.connection import get_pool as get_el_pool


class FlaskPhiloTestCase(object):
    """
    This tests should be used when testing views
    """

    def setup(self):
        if self.app is None:
            self.app = flask.current_app
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
