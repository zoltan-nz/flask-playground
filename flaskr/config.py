from os import getenv


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "dev"
    DATABASE_URI = "file::memory:?cache=shared"

    def __init__(self):
        self.PORT = getenv("PORT", "5000")


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "./db/development.sqlite"


class RunningTestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DATABASE_URI = getenv("FLASKR_DATABASE_URI", "./db/production.sqlite")

    def __init__(self):
        super().__init__()
        secret_key = getenv("FLASKR_SECRET_KEY")
        if secret_key is None:
            raise ValueError(
                "Invalid secret key. FLASKR_SECRET_KEY environment variable is missing."
            )
        self.SECRET_KEY = secret_key


def get_config(environment):
    config_map = {
        "test": lambda: RunningTestConfig(),
        "development": lambda: DevelopmentConfig(),
        "production": lambda: ProductionConfig(),
    }

    config = config_map.get(environment)
    if config is None:
        raise ValueError(f"Invalid environment: {environment}")
    return config()
