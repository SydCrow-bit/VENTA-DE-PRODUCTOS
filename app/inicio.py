from flask import Blueprint, render_template
from flask_login import login_required, current_user

inicio_bp = Blueprint("inicio", __name__)

@inicio_bp.route("/inicio")
@login_required
def inicio():

    rol = current_user.role

    return render_template("inicio/inicio.html", rol=rol)