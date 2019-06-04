from os import getenv, makedirs

from flask import Flask

from flaskr import db, auth, blog
from flaskr.config import get_config


def create_app(test_config=None):
    app = Flask(__name__)

    try:
        if test_config is not None:
            environment = "test"
        else:
            environment = getenv("FLASK_ENV")
        app.config.from_object(get_config(environment))
    except ValueError as e:
        print(e)
        exit(1)

    @app.route("/health-check")
    def health_check():
        return "FLASKR app is running."

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule("/", endpoint="index")

    print(app.config)
    return app
