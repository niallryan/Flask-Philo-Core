from flask_philo_core.views import BaseView
from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from flask import json


class SimpleView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok'})


class SimpleCorsView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok-cors'})


URLS = (
    ('/', SimpleView, 'home'),
    ('/cors-api/test-cors', SimpleCorsView, 'cors'),
)


class TestViews(FlaskPhiloTestCase):
    def test_urls(self):
        app = BaseTestFactory.create_test_app()
        assert 'URLS' not in app.config
        rules = [r for r in app.url_map.iter_rules()]
        endpoints = [rl.endpoint for rl in rules]
        assert 1 == len(endpoints)
        assert 'static' in endpoints

        app = BaseTestFactory.create_test_app(urls=URLS)

        assert 'URLS' in app.config
        rules2 = [r for r in app.url_map.iter_rules()]
        endpoints2 = [rl.endpoint for rl in rules2]
        assert 3 == len(endpoints2)
        assert 'cors' in endpoints2
        assert 'static' in endpoints2
        assert 'home' in endpoints2

    def test_simple_view(self):
        app = BaseTestFactory.create_test_app(urls=URLS)
        client = app.test_client()
        result = client.get('/')
        assert 200 == result.status_code
        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in j_content
        assert 'ok' == j_content['msg']

    def test_cors(self):
        config = {}
        config['CORS'] = {
            r"/cors-api/*": {"origins": "FLASK_PHILO_CORE_TEST_CORS"}}
        app = BaseTestFactory.create_test_app(config=config, urls=URLS)
        client = app.test_client()
        result = client.get('/cors-api/test-cors')
        assert 'Access-Control-Allow-Origin' in result.headers
        cors_val = result.headers['Access-Control-Allow-Origin']
        assert 'FLASK_PHILO_CORE_TEST_CORS' == cors_val
        assert 200 == result.status_code

        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in j_content
        assert 'ok-cors' == j_content['msg']
