from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    g,
    redirect,
    url_for,
    abort,
    current_app)

from flaskr.auth import login_required
from flaskr.db import get_db

BLOG_BP = Blueprint("blog", __name__)


@BLOG_BP.route("/")
def index():
    database = get_db()
    posts = database.execute(
        """\
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC
        """
    ).fetchall()

    flaskr_image_name = current_app.config["FLASKR_IMAGE_NAME"]

    return render_template("blog/index.html", posts=posts, flaskr_image_name=flaskr_image_name)


@BLOG_BP.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            database = get_db()
            database.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            database.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):  # pylint: disable=redefined-builtin
    post = (
        get_db()
        .execute(
            """\
                SELECT p.id, title, body, created, author_id, username
                FROM post p JOIN user u ON p.author_id = u.id
                WHERE p.id = ?
            """,
            id,
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@BLOG_BP.route("/<id>/update", methods=("GET", "POST"))
@login_required
def update(id):  # pylint: disable=redefined-builtin
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@BLOG_BP.route("/<id>/delete", methods=["POST"])
@login_required
def delete(id):  # pylint: disable=redefined-builtin
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", id)
    db.commit()
    return redirect(url_for("blog.index"))
