Flask-Philo-Core Views
==========================

Most of the applications we build with Flask-Philo-Core are simple REST APIs.
You can use Flask-Philo-Core to do more complicated things but the most common thing
we do is return blocks oj JSON from REST endpoints.

We keep most of our appications views in a ``views.py`` file in ``src/app``.

They all inherit from ``flask_philo.views.BaseResourceView``.


Here's an example view for a GET endpoint that returns a simple JSON message:

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




The next thing to do is create some tuple values in ``src/app/urls.py`` to specify
the url for the endpoint you want to expose:

E.g.

::

    from app.views import SimpleView, SimpleCorsView

    URLS = (
      ('/', SimpleView, 'home'),
      ('/cors-api/test-cors', SimpleCorsView, 'cors'),
    )


Now, when you run the server and make a GET request to ``/``,
the application should respond with a status of ``200`` and ``ok``.


CORS support
----------------------------------------------

 We rely on the *resource specific* feature provided by
`flask-cors <https://flask-cors.readthedocs.io/en/latest/#resource-specific-cors>`_ to
bring  CORS support to Flask-Philo-Core.

You will need to define the url patterns in your configuration file:

::

    CORS = {r"/cors-api/*": {"origins": "*"}



JSON Serializers
---------------------------------------------------------

A serializer is a mechanism that we use in Flask-Philo-Core to serialize and deserialize
data in a safe way. The main principle behind serializers is that data sent by users can
not be trusted by default. To create a serializer you must inherit from 
``flask_philo_core.serializers.BaseSerializer`` and define the ``_shcema`` property
following the rules specified in `jsonschema <http://json-schema.org/>`_

E.g.

::

    class TransactionSerializer(BaseSerializer):
        _schema = {
            'type': 'object',

            'definitions': {
                'vin_schema': input_schema,
                'vout_schema': output_schema
            },

            'properties': {
                'key': uuid_schema,
                'key2': uuid_schema,
                'txid': alphanumeric_schema,
                'hash': alphanumeric_schema,
                'vout':
                    {'type': 'array', 'items': {'$ref': '#/definitions/vout_schema'}},
                'vin': {'$ref': '#/definitions/vin_schema'},
            }
        }




    tx_data = {
        'key': uuid.uuid4(),
        'hash': format(randint(0, 99999), '02x'),
        'txid': BaseTestFactory.create_unique_string(),
        'vin': input_data,
        'key2': uuid.uuid4(),
        'vout': output_data
    }

    serializer = TransactionSerializer(data=tx_data)
    print(serializer.json)
