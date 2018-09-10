#from flask_philo import flask.current_app
import flask
from flask import abort, json, render_template, make_response, Response, g
from flask.views import MethodView


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.app = flask.current_app
        super(BaseView, self).__init__(*args, **kwargs)

    def __init__1(self, *args, **kwargs):

        # assign postgresql pool connections
        if 'DATABASES' in flask.current_app.config and\
                'POSTGRESQL' in flask.current_app.config['DATABASES']:
            if hasattr(g, 'postgresql_pool'):
                self.postgresql_pool = g.postgresql_pool

        # assign redis pool connections
        if 'DATABASES' in flask.current_app.config and 'REDIS' in flask.current_app.config['DATABASES']:
            if hasattr(g, 'redis_pool'):
                self.redis_pool = g.redis_pool

        if 'JINJA2_TEMPLATES' in flask.current_app.config:
            if hasattr(g, 'jinja2_template_manager'):
                self.jinja2_template_manager = g.jinja2_template_manager
        super(BaseView, self).__init__(*args, **kwargs)

    def json_response(self, status=200, data={}, headers={}):
        """
        Json response that allows headers injection
        """
        '''
          To set flask to inject specific headers on response request,
          such as CORS_ORIGIN headers
        '''
        mimetype = 'application/json'
        header_dict = {}

        for k, v in headers.items():
            header_dict[k] = v

        # setting custon headers for CORS origin
        if flask.current_app.config.get("ALLOW_ORIGIN", None):
            header_dict["Access-Control-Allow-Origin"] = flask.current_app.config["ALLOW_ORIGIN"] # noqa

        if flask.current_app.config.get("ALLOW_HEADERS", None):
            header_dict["Access-Control-Allow-Headers"] = flask.current_app.config["ALLOW_HEADERS"] # noqa

        if flask.current_app.config.get("ALLOW_METHODS", None):
            header_dict["Access-Control-Allow-Methods"] = flask.current_app.config["ALLOW_METHODS"] # noqa
        return Response(
            json.dumps(data),
            status=status,
            mimetype=mimetype,
            headers=header_dict)

    def render_template(self, template_name, engine_name='DEFAULT', **values):
        if not hasattr(self, 'jinja2_template_manager'):
            return render_template(template_name, **values)
        else:
            return self.jinja2_template_manager.render(
                template_name, **values)

    def template_response(self, template_name, headers={}, **values):
        """
        Constructs a response, allowing custom template name and content_type
        """
        response = make_response(
            self.render_template(template_name, **values))

        for field, value in headers.items():
            response.headers.set(field, value)

        return response

    def get(self, *args, **kwargs):
        abort(400)

    def post(self, *args, **kwargs):
        abort(400)

    def put(self, *args, **kwargs):
        abort(400)

    def patch(self, *args, **kwargs):
        abort(400)

    def delete(self, *args, **kwargs):
        abort(400)


class BaseResourceView(BaseView):

    def get(self, *args, **kwargs):
        return self.json_response(400)

    def post(self, *args, **kwargs):
        return self.json_response(400)

    def put(self, *args, **kwargs):
        return self.json_response(400)

    def patch(self, *args, **kwargs):
        return self.json_response(400)

    def delete(self, *args, **kwargs):
        return self.json_response(400)
