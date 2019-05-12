import pytest

from flaskr import create_app


@pytest.fixture
def app():
    test_app = create_app({"TESTING": True})
    yield test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get("/health-check")
    assert b"FLASKR app is running." in response.data
