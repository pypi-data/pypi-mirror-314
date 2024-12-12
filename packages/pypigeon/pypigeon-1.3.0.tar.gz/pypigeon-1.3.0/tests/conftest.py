import pytest
from pypigeon.pigeon_core import AuthenticatedClient


@pytest.fixture
def client():
    return AuthenticatedClient(
        base_url="https://pigeon.test/api/v1", token="test-token"
    )
