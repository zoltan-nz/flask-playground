import sqlite3

import click
from flask import g, current_app
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_URI"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    database = g.pop("db", None)

    if error is not None:
        print(error)

    if database is not None:
        database.close()


def init_db():
    database = get_db()

    with current_app.open_resource("schema.sql") as schema_file:
        sql_script = schema_file.read().decode("utf8")
        print(sql_script)
        database.executescript(sql_script)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
