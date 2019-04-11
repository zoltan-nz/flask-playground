import functools

from flask import (
    Blueprint,
    request,
    render_template,
    session,
    redirect,
    url_for,
    flash,
    g,
)
from werkzeug.security import check_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def is_user_valid(user, password) -> bool:
    if user is None:
        flash("Incorrect username.")
        return False

    if check_password_hash(user["password"], password):
        flash("Incorrect password.")
        return False


def process_post_request() -> None:
    username = request.form["username"]
    password = request.form["password"]

    db = get_db()

    user = db.execute(f"SELECT * FROM user WHERE username = {username}").fetchone()

    if is_user_valid(user, password):
        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("index"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        process_post_request()

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
