# =========================================================
# IMPORTANTE PARA TODO EL GRUPO: SEGURIDAD DE RUTAS
# =========================================================
# 1. IMPORTACIÓN:
#    Para usar los decoradores de seguridad, asegúrate de 
#    incluir esta línea al inicio de tu archivo:
#    from .decorators import admin_required, referrer_required
#
# 2. USO DE DECORADORES:
#    - @login_required: Verifica que el usuario esté logueado.
#    - @admin_required: Verifica que el usuario tenga rol "admin".
#    - @referrer_required: Bloquea el acceso manual desde la URL 
#      (exige que el usuario venga de un clic interno, ej. Login).
#
# 3. EJEMPLO DE IMPLEMENTACIÓN EN CRUDs:
#
#    @admin_bp.route("/usuarios")
#    @login_required
#    @admin_required
#    @referrer_required
#    def gestion_usuarios():
#        ...
#
# =========================================================
# NOTA IMPORTANTE:
# @referrer_required permite la navegación interna. Una vez
# que el usuario entra legalmente desde el Login, puede 
# moverse por todos los menús. Solo se bloquea si intenta
# pegar la URL directamente en una pestaña nueva.
# =========================================================

# =========================================================

from .decorators import admin_required, referrer_required


from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from .models import User
from .extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# =========================
# DASHBOARD
# =========================

@admin_bp.route("/")
@login_required
@admin_required
@referrer_required

def dashboard():
    return render_template("admin.usuarios")


# =========================
# LISTAR USUARIOS (READ)
# =========================

@admin_bp.route("/usuarios")
@login_required
@admin_required
@referrer_required

def usuarios():

    usuarios = User.query.all()

    return render_template("admin/usuarios.html", usuarios=usuarios)


# =========================
# CREAR USUARIO (CREATE)
# =========================

@admin_bp.route("/usuarios/crear", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required

def crear_usuario():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        usuario = User(username=username, role=role)
        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()
        flash("Nuevo usuario creado con éxito", "success")

        return redirect(url_for("admin.usuarios"))

    return render_template("admin/crear_usuario.html")


# =========================
# EDITAR USUARIO (UPDATE)
# =========================

@admin_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required

def editar_usuario(id):

    usuario = User.query.get_or_404(id)
    nombre = usuario.username

    if request.method == "POST":

        usuario.username = request.form.get("username")
        usuario.role = request.form.get("role")

        db.session.commit()
        
        flash(f"Usuario '{nombre}' editado correctamente", "success")

        return redirect(url_for("admin.usuarios"))

    return render_template("admin/editar_usuario.html", usuario=usuario)


# =========================
# ELIMINAR USUARIO (DELETE)
# =========================

@admin_bp.route("/usuarios/eliminar/<int:id>")
@login_required
@admin_required
@referrer_required

def eliminar_usuario(id):

    usuario = User.query.get_or_404(id)
    nombre = usuario.username

    db.session.delete(usuario)
    db.session.commit()
    
    flash(f"Usuario '{nombre}' eliminado correctamente", "success")

    return redirect(url_for("admin.usuarios"))

# =========================
# INTEGRACIÓN DE CHAT BOT
# =========================

@admin_bp.route("/chat")
@login_required
@admin_required
@referrer_required
def chat():
    return render_template("admin/chat.html")

#-----------------------------------------
