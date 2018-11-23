Unit Tests
=============================================


Flask-Philo-Core provides support for unit testing through the library
`pytest <https://docs.pytest.org/en/latest/>`_.


Writing Unit Tests with Flask-Philo-Core
-----------------------------------------------------



The class ``flask_philo_core.test.FlaskPhiloTestCase`` provides common
functionality to implement unit testing in your application. 

E.g.

::

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



Mocking Configuration
---------------------------------

We use the `unittest.mock  <https://docs.python.org/3/library/unittest.mock.html>`_
library to mock the Flask-Philo-Core configuration object.

The following example shows how to use the
``flask_philo_core.test.BaseTestFactory.create_test_app`` function to create a
Flask-Philo-Core application for unit testing:


::

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


The ``flask_philo_core.test.BaseTestFactory.create_test_app`` function expects
two optional parameters:

* config: dictionary with the configuration options to mock.

* URLS: tuple to mock the ``urls.py`` file.



Running Unit Tests
--------------------

To run all Unit Tests for a Flask-Philo-Core app, use the following console
command:

::

    flask-philo test



To execute *only* the Unit Tests from one **source file**, use the ``--q <test_source.py>`` argument:

::

    flask-philo test --q tests/test_db.py


To execute *only* the tests from one **class** :


::

    flask-philo test --q tests/test_db.py::TestDBAccess


To execute a single specific unit test :

::

    flask-philo test --q tests/test_db.py::TestDBAccess::test_create_index
