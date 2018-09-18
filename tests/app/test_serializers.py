from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from flask_philo_core.serializers import (
    uuid_schema, alphanumeric_schema, BaseSerializer
)
from .test_app import create_app

from decimal import Decimal
from flask import json
from jsonschema.exceptions import ValidationError
from random import randint

import pytest
import uuid


input_schema = {
    'type': 'object',
    'properties': {
        'key': uuid_schema,
        'key2': uuid_schema,
        'coinbase': alphanumeric_schema,
        'sequence': {'type': 'number'}
    }
}


inner_output_schema = {
    'type': 'object',
    'properties': {
        'key': uuid_schema,
    }
}


output_schema = {
    'type': 'object',
    'definitions': {
        'inner_output': inner_output_schema
    },
    'properties': {
        'key': uuid_schema,
        'inner_output': inner_output_schema,
        'value': {'type': 'number'},
        'n': {'type': 'number'},

    }
}


transaction_schema = {
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
        'vout': {'type': 'array', 'items': {'$ref': '#/definitions/vout_schema'}},
        'vin': {'$ref': '#/definitions/vin_schema'},
    }
}


class InputSerializer(BaseSerializer):
    _schema = input_schema


class OutputSerializer(BaseSerializer):
    _schema = output_schema


class TransactionSerializer(BaseSerializer):
    _schema = transaction_schema


class TestSerializers(FlaskPhiloTestCase):
    def setup(self):
        self.app = create_app()
        super(TestSerializers, self).setup()

    def test_simple_object(self):
        data = {
            'key': uuid.uuid4(),
            'coinbase': BaseTestFactory.create_unique_string(),
            'sequence': randint(0, 99999)
        }
        serializer = InputSerializer(data=data)
        assert data == serializer.json

        payload = json.dumps(data)
        serializer2 = InputSerializer(payload=payload)
        assert serializer2.json.keys() == serializer.json.keys()
        assert payload == serializer.dumps()

        # for security reasons should not accept additional parameters
        new_data = data.copy()
        new_data['unknown'] = 'invalid'
        with pytest.raises(ValidationError):
            InputSerializer(data=new_data)

    def test_decimal(self):
        data = {
            'key': uuid.uuid4(),
            'value': BaseTestFactory.create_random_decimal(),
            'n': randint(0, 99999)
        }
        serializer = OutputSerializer(data=data)
        payload = serializer.dumps()
        serializer2 = OutputSerializer(payload=payload)
        assert serializer2.json.keys() == serializer.json.keys()
        assert Decimal == type(serializer.json['value'])
        assert Decimal == type(serializer2.json['value'])

    def test_nested_object(self):
        input_data = {
            'key': uuid.uuid4(),
            'key2': uuid.uuid4(),
            'coinbase': BaseTestFactory.create_unique_string(),
            'sequence': randint(0, 99999)
        }

        output_data = [
            {
                'key': uuid.uuid4(),
                'value': BaseTestFactory.create_random_decimal(),
                'n': randint(0, 99999),
                'inner_output': {'key': uuid.uuid4()},
            },

            {
                'key': uuid.uuid4(),
                'value': BaseTestFactory.create_random_decimal(),
                'n': randint(0, 99999)
            },

        ]

        tx_data = {
            'key': uuid.uuid4(),
            'hash': format(randint(0, 99999), '02x'),
            'txid': BaseTestFactory.create_unique_string(),
            'vin': input_data,
            'key2': uuid.uuid4(),
            'vout': output_data
        }

        serializer = TransactionSerializer(data=tx_data)
        k1 = output_data[0]['inner_output']['key']
        k2 = serializer.json['vout'][0]['inner_output']['key']
        assert  k1 == k2
