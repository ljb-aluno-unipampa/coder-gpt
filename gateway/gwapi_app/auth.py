from functools import wraps
from flask import Blueprint, request, session, redirect, url_for, render_template, current_app

auth_bp = Blueprint("auth", __name__)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == current_app.config["ADMIN_USER"] and password == current_app.config["ADMIN_PASSWORD"]:
            session["authenticated"] = True
            return redirect("/")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
