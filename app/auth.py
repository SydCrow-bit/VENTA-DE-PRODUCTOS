from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from .extensions import login_manager, db

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/")
def inicio():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        usuario = User.query.filter_by(username=username).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for("inicio.inicio"))

        flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for('auth.register'))

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("El nombre de usuario ya existe", "error")
            return redirect(url_for('auth.register'))

        nuevo_usuario = User(username=username, role='user')
        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')