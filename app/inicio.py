from .decorators import admin_required, referrer_required
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

inicio_bp = Blueprint("inicio", __name__)

@inicio_bp.route("/inicio")
@login_required
@referrer_required
def inicio():
    rol = current_user.role

    return render_template("inicio/inicio.html", rol=rol)