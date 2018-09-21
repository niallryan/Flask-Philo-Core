from flask_philo_core import init_cors, init_urls
from flask_philo_core.views import BaseView
from flask_philo_core.test import FlaskPhiloTestCase
from unittest.mock import patch
from flask import json


class SimpleView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok'})


class SimpleCorsView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok-cors'})


class TestViews(FlaskPhiloTestCase):
    def setup(self):
        self.base_mock_config['URLS'] = 'app.urls'
        super(TestViews, self).setup()

    def test_simple_view(self):
        with patch.dict(self.app.config, self.base_mock_config):
            init_urls(self.app)
            result = self.client.get('/')
            assert 200 == result.status_code
            j_content = json.loads(result.get_data().decode('utf-8'))
            assert 'msg' in j_content
            assert 'ok' == j_content['msg']

    def test_cors(self):
        config = self.base_mock_config.copy()

        config['CORS'] = {
            r"/cors-api/*": {"origins": "FLASK_PHILO_CORE_TEST_CORS"}}

        with patch.dict(self.app.config, config):
            init_urls(self.app)
            init_cors(self.app)
            result = self.client.get('/cors-api/test-cors')
            assert 'Access-Control-Allow-Origin' in result.headers
            cors_val = result.headers['Access-Control-Allow-Origin']
            assert 'FLASK_PHILO_CORE_TEST_CORS' == cors_val
            assert 200 == result.status_code

            j_content = json.loads(result.get_data().decode('utf-8'))
            assert 'msg' in j_content
            assert 'ok-cors' == j_content['msg']
