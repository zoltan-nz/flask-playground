import pytest

from flaskr import create_app


@pytest.fixture
def app():
    test_app = create_app({"TESTING": True})
    yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/hello")
    assert b"Hello" in response.data
