from flask_philo_core.views import BaseView
from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from jinja2 import nodes
from jinja2.ext import Extension

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

JINJA2_TEMPLATES = {
    'path': (
        os.path.join(BASE_DIR, 'templates_test_philo'),
    ),
    'encoding': 'utf-8',
    'followlinks': False,
    'AUTOESCAPING': {
        'enabled_extensions': ('html', 'htm', 'xml'),
        'disabled_extensions': [],
        'default_for_string': True,
        'default': False
    },
    'EXTENSIONS': (
        'app.test_jinja2.SimpleExtension',
    )
}


class SimpleView(BaseView):
    def get(self, template_location):
        template_name = '{0}/template_view.html'.format(template_location)
        return self.render_template(
            template_name, template_location=template_location)


URLS = (
    ('/<template_location>', SimpleView, 'home'),
)


class SimpleExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['testtag'])

    def __init__(self, environment):
        super(SimpleExtension, self).__init__(environment)

    def _testtag(self, msg, caller):
        return '{} hello world!!!'.format(msg)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endtesttag'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method(
                '_testtag', args), [], [], body).set_lineno(lineno)


class TestJinja2(FlaskPhiloTestCase):

    def test_jinja2_loader(self):
        """
        Test loader from filesystem
        """
        app = BaseTestFactory.create_test_app(
            config={'JINJA2_TEMPLATES': JINJA2_TEMPLATES})
        env = app.jinja_env
        assert 5 == len(env.list_templates())
        assert 'index.html' == env.list_templates()[0]
        assert 'templates1/index.html' == env.list_templates()[1]

    def test_load_templates(self):
        """
        test if templates are loaded correctly
        """
        app = BaseTestFactory.create_test_app(
            config={'JINJA2_TEMPLATES': JINJA2_TEMPLATES})
        env = app.jinja_env
        template_idx1 = env.get_template('templates1/index.html')
        template_idx2 = env.get_template('templates2/index.html')
        idx1 = template_idx1.render({'msg_1': 'hello template1'})
        idx2 = template_idx2.render({'msg_2': 'hello template2'})
        assert idx1 == 'hello template1'
        assert idx2 == 'hello template2'

    def test_custom_tag(self):
        app = BaseTestFactory.create_test_app(
            config={'JINJA2_TEMPLATES': JINJA2_TEMPLATES})
        env = app.jinja_env
        template = env.get_template('index.html')
        txt = template.render()
        assert 'random_msg hello world!!!' == txt

    def test_template_view(self):
        app = BaseTestFactory.create_test_app(
            config={'JINJA2_TEMPLATES': JINJA2_TEMPLATES}, urls=URLS)
        client = app.test_client()

        result = client.get('/templates1')
        assert 200 == result.status_code
        assert '<h1>templates1</h1>' == result.get_data().decode('utf-8')

        result = client.get('/templates2')
        assert 200 == result.status_code
        assert '<h1>templates2</h1>' == result.get_data().decode('utf-8')
