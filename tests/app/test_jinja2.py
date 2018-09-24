from flask_philo_core.test import FlaskPhiloTestCase
from jinja2 import nodes
from jinja2.ext import Extension
from unittest.mock import patch

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
            self.call_method('_testtag', args), [], [], body).set_lineno(lineno)


class TestJinja2(FlaskPhiloTestCase):
    def setup(self):
        self.mock_config['JINJA2_TEMPLATES'] = JINJA2_TEMPLATES
        super(TestJinja2, self).setup()


    def test_jinja2_loader(self):
        """
        Test loader from filesystem
        """
        with patch.dict(
            self.app.config, {'JINJA2_TEMPLATES': JINJA2_TEMPLATES}):
            env = self.app.jinja_env
            assert 3 == len(env.list_templates())
            assert 'index.html' == env.list_templates()[0]
            assert 'templates1/index.html' == env.list_templates()[1]
            assert 'templates2/index.html' == env.list_templates()[2]


    def test_load_templates(self):
        """
        test if templates are loaded correctly
        """
        with patch.dict(
            self.app.config, {'JINJA2_TEMPLATES': JINJA2_TEMPLATES}):
            env = self.app.jinja_env
            template_idx1 = env.get_template('templates1/index.html')
            template_idx2 = env.get_template('templates2/index.html')
            idx1 = template_idx1.render({'msg_1': 'hello template1'})
            idx2 = template_idx2.render({'msg_2': 'hello template2'})
            assert idx1 == 'hello template1'
            assert idx2 == 'hello template2'


    def test_custom_tag(self):
        with patch.dict(
            self.app.config, {'JINJA2_TEMPLATES': JINJA2_TEMPLATES}):
            env = self.app.jinja_env
            template = env.get_template('index.html')
            txt = template.render()
            assert 'random_msg hello world!!!' == txt
