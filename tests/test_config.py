import pytest

from flaskr.config import get_config, Config, DevelopmentConfig, RunningTestConfig


def test_get_config_with_invalid_environment():
    with pytest.raises(ValueError) as raised_exception:
        get_config("")
    assert "Invalid environment:" in str(raised_exception.value)

    with pytest.raises(ValueError) as raised_exception:
        get_config("bar")
    assert "Invalid environment: bar" in str(raised_exception.value)

    with pytest.raises(ValueError) as raised_exception:
        get_config("production")
    assert "Invalid secret key." in str(raised_exception.value)


def test_defaults():
    config = Config()
    assert config.DEBUG is False
    assert config.TESTING is False
    assert config.SECRET_KEY == "dev"
    assert config.DATABASE_URI == "file::memory:?cache=shared"
    assert config.PORT == "5000"


def test_port(monkeypatch):
    monkeypatch.setenv("PORT", "1234")
    config = DevelopmentConfig()
    assert config.PORT == "1234"

    monkeypatch.setenv("FLASKR_SECRET_KEY", "secret")
    production_config = get_config("production")
    assert production_config.PORT == "1234"


def test_development_config():
    config = get_config("development")
    assert config.DEBUG is True
    assert config.TESTING is False
    assert config.SECRET_KEY == "dev"


def test_test_config():
    config = RunningTestConfig()
    assert config.TESTING is True
    assert config.PORT == "5000"


def test_secret_key(monkeypatch):
    monkeypatch.setenv("FLASKR_SECRET_KEY", "secret")
    config = get_config("production")
    assert config.SECRET_KEY == "secret"
