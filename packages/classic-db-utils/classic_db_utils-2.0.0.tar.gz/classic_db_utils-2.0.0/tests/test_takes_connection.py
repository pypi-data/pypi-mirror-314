from unittest.mock import MagicMock

import pytest

from classic.db_utils import takes_connection


class SomeClass:
    def __init__(self, connect, my_connect):
        self.connect = connect
        self.my_connect = my_connect

    @takes_connection
    def some_method(self, connection):
        return connection

    @takes_connection(connect_attr='my_connect', connection_param='conn')
    def custom_method(self, conn):
        return conn


@pytest.fixture
def connect():
    connect = MagicMock()
    connect.return_value.__enter__.return_value = 'test_connection'
    connect.return_value.__exit__.return_value = None
    return connect


@pytest.fixture
def custom_connect():
    connect = MagicMock()
    connect.return_value.__enter__.return_value = 'custom_connection'
    connect.return_value.__exit__.return_value = None
    return connect


@pytest.fixture
def some_class_obj(connect, custom_connect):
    return SomeClass(
        connect=connect,
        my_connect=custom_connect,
    )


def test_decorator_with_default_attrs(some_class_obj):
    result = some_class_obj.some_method()

    assert result == 'test_connection'
    some_class_obj.connect.assert_called_once()


def test_decorator_with_custom_names(some_class_obj):
    result = some_class_obj.custom_method()

    assert result == 'custom_connection'
    some_class_obj.my_connect.assert_called_once()
