from flask_philo_core.views import BaseView
from flask_philo_core.test import FlaskPhiloTestCase
from .test_app import create_app
import simplejson as json
import flask

class SimpleView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok'})

class SimpleCorsView(BaseView):
    def get(self):
        return self.json_response(data={'msg': 'ok-cors'})


class TestViews(FlaskPhiloTestCase):
    def setup(self):
        self.app = create_app()
        super(TestViews, self).setup()

    def test_simple_view(self):
        result = self.client.get('/')
        assert 200 == result.status_code
        j_content = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in j_content
        assert 'ok' == j_content['msg']

    def test_cors(self):
        result = self.client.get('/cors-api/test-cors')
        assert 'Access-Control-Allow-Origin' in result.headers
        cors_val = result.headers['Access-Control-Allow-Origin']
        assert 'FLASK_PHILO_CORE_TEST_CORS' == cors_val
