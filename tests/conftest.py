import pytest

from portia.main import app


@pytest.fixture()
def client():
    return app.test_client()
