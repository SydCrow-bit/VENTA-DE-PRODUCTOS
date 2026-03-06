from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from .models import User
from .extensions import login_manager, db

auth_bp = Blueprint("auth", __name__)

# Flask-Login necesita esto para cargar usuarios
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Ruta principal
@auth_bp.route("/")
def inicio():
    return redirect(url_for("auth.login"))


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print("Usuario ingresado:", username)
        print("Password ingresado:", password)

        usuario = User.query.filter_by(username=username).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect("/admin")

    return render_template("login.html")


# LOGOUT
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))