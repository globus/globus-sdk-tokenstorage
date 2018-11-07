import json
import os
import shutil
import tempfile
import time

import pytest

from globus_sdk_tokenstorage import SimpleJSONFileAdapter, __version__

try:
    import mock
except ImportError:
    from unittest import mock


@pytest.fixture
def tempdir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


@pytest.fixture
def filename(tempdir):
    return os.path.join(tempdir, "mydata.json")


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
    "success, kwargs",
    [
        (False, {}),
        (False, {"resource_server": "foo", "scopes": ["bar"]}),
        (True, {"resource_server": "foo"}),
        (True, {"scopes": ["bar"]}),
    ],
)
def test_constructor(filename, success, kwargs):
    if success:
        assert SimpleJSONFileAdapter(filename, **kwargs)
    else:
        with pytest.raises(ValueError):
            SimpleJSONFileAdapter(filename, **kwargs)


def test_file_dne(filename):
    adapter = SimpleJSONFileAdapter(filename, scopes=["x"])
    assert not adapter.file_exists()


def test_file_exists(filename):
    open(filename, "w").close()  # open and close to touch
    adapter = SimpleJSONFileAdapter(filename, scopes=["x"])
    assert adapter.file_exists()


def test_read_as_dict(filename):
    with open(filename, "w") as f:
        json.dump({"x": 1}, f)
    adapter = SimpleJSONFileAdapter(filename, scopes=["x"])
    assert adapter.file_exists()

    d = adapter.read_as_dict()

    assert d == {"x": 1}


def test_store(filename, mock_response):
    adapter = SimpleJSONFileAdapter(filename, resource_server="resource_server_1")
    assert not adapter.file_exists()
    adapter.store(mock_response)

    # mode|0600 should be 0600 -- meaning that those are the maximal
    # permissions given
    st_mode = os.stat(filename).st_mode & 0o777  # & 777 to remove extra bits
    assert st_mode | 0o600 == 0o600

    with open(filename, "r") as f:
        data = json.load(f)
    assert data["globus-sdk-tokenstorage.version"] == __version__
    assert data["access_token"] == "access_token_1"
