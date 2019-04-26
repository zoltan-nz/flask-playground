import os
from pathlib import Path

from flask import Flask

from flaskr import db, auth, blog


def create_app(test_config=None, *args, **kwargs):
    port = int(os.environ.get('PORT', 5000))

    print(f"test_config={test_config}\n"
          f"args={args}\n"
          f"kwargs={kwargs}\n"
          f"port={port}")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=Path(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
