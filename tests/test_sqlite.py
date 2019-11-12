import os
import shutil
import tempfile
import time

import pytest
from globus_sdk_tokenstorage import SQLiteAdapter

try:
    import mock
except ImportError:
    from unittest import mock  # type: ignore


IS_WINDOWS = os.name == "nt"

MEMORY_DBNAME = ":memory:"


@pytest.fixture
def tempdir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


@pytest.fixture
def db_filename(tempdir):
    return os.path.join(tempdir, "test.db")


@pytest.fixture
def mock_response():
    res = mock.Mock()
    expiration_time = int(time.time()) + 3600
    res.by_resource_server = {
        "resource_server_1": {
            "access_token": "access_token_1",
            "expires_at_seconds": expiration_time,
            "refresh_token": "refresh_token_1",
            "resource_server": "resource_server_1",
            "scope": "scope1",
            "token_type": "bearer",
        },
        "resource_server_2": {
            "access_token": "access_token_2",
            "expires_in": expiration_time,
            "refresh_token": "refresh_token_2",
            "resource_server": "resource_server_2",
            "scope": "scope2 scope2:0 scope2:1",
            "token_type": "bearer",
        },
    }
    return res


@pytest.mark.parametrize(
    "success, use_file, kwargs",
    [
        (False, False, {}),
        (False, False, {"namespace": "foo"}),
        (True, False, {"dbname": MEMORY_DBNAME}),
        (True, False, {"dbname": MEMORY_DBNAME, "namespace": "foo"}),
        (True, True, {}),
        (True, True, {"namespace": "foo"}),
        (False, True, {"dbname": MEMORY_DBNAME}),
        (False, True, {"dbname": MEMORY_DBNAME, "namespace": "foo"}),
    ],
)
def test_constructor(success, use_file, kwargs, db_filename):
    if success:
        if use_file:
            assert SQLiteAdapter(db_filename, **kwargs)
        else:
            assert SQLiteAdapter(**kwargs)
    else:
        with pytest.raises(TypeError):
            if use_file:
                SQLiteAdapter(db_filename, **kwargs)
            else:
                SQLiteAdapter(**kwargs)


def test_store_and_retrieve_simple_config():
    adapter = SQLiteAdapter(MEMORY_DBNAME)
    store_val = {"val1": True, "val2": None, "val3": 1.4}
    adapter.store_config("myconf", store_val)
    read_val = adapter.read_config("myconf")
    assert read_val == store_val
    assert read_val is not store_val


def test_store_and_retrieve(mock_response):
    adapter = SQLiteAdapter(MEMORY_DBNAME)
    adapter.store(mock_response)

    data = adapter.read_as_dict()
    assert data == mock_response.by_resource_server


def test_on_refresh_and_retrieve(mock_response):
    """just confirm that the aliasing of these functions does not change anything"""
    adapter = SQLiteAdapter(MEMORY_DBNAME)
    adapter.on_refresh(mock_response)

    data = adapter.read_as_dict()
    assert data == mock_response.by_resource_server


def test_multiple_adapters_store_and_retrieve(mock_response, db_filename):
    adapter1 = SQLiteAdapter(db_filename)
    adapter2 = SQLiteAdapter(db_filename)
    adapter1.store(mock_response)

    data = adapter2.read_as_dict()
    assert data == mock_response.by_resource_server


def test_multiple_adapters_store_and_retrieve_different_namespaces(
    mock_response, db_filename
):
    adapter1 = SQLiteAdapter(db_filename, namespace="foo")
    adapter2 = SQLiteAdapter(db_filename, namespace="bar")
    adapter1.store(mock_response)

    data = adapter2.read_as_dict()
    assert data == {}


def test_load_missing_config_data():
    adapter = SQLiteAdapter(MEMORY_DBNAME)
    assert adapter.read_config("foo") is None


def test_load_missing_token_data():
    adapter = SQLiteAdapter(MEMORY_DBNAME)
    assert adapter.read_as_dict() == {}
