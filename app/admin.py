from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from .models import User
from .extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# =========================
# DASHBOARD
# =========================

@admin_bp.route("/")
@login_required
def dashboard():
    return render_template("admin/dashboard.html")


# =========================
# LISTAR USUARIOS (READ)
# =========================

@admin_bp.route("/usuarios")
@login_required
def usuarios():

    usuarios = User.query.all()

    return render_template("admin/usuarios.html", usuarios=usuarios)


# =========================
# CREAR USUARIO (CREATE)
# =========================

@admin_bp.route("/usuarios/crear", methods=["GET", "POST"])
@login_required
def crear_usuario():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        usuario = User(username=username, role=role)
        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("admin.usuarios"))

    return render_template("admin/crear_usuario.html")


# =========================
# EDITAR USUARIO (UPDATE)
# =========================

@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):

    usuario = User.query.get_or_404(id)

    if request.method == "POST":

        usuario.username = request.form.get("username")
        usuario.role = request.form.get("role")

        db.session.commit()

        return redirect(url_for("admin.usuarios"))

    return render_template("admin/editar_usuario.html", usuario=usuario)


# =========================
# ELIMINAR USUARIO (DELETE)
# =========================

@admin_bp.route("/usuarios/eliminar/<int:id>")
@login_required
def eliminar_usuario(id):

    usuario = User.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for("admin.usuarios"))