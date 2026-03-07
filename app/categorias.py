from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import Categoria
from .extensions import db
from .decorators import admin_required, referrer_required

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")

@categorias_bp.route("/")
@login_required
@referrer_required
def index():
    categorias = Categoria.query.all()
    return render_template("categorias/index.html", categorias=categorias)

@categorias_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required
def create():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        
        nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_categoria)
        db.session.commit()
        
        flash("Categoria creada exitosamente", "success")
        return redirect(url_for("categorias.index"))

    return render_template("categorias/create.html")

@categorias_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required
def edit(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == "POST":
        categoria.nombre = request.form.get("nombre")
        categoria.descripcion = request.form.get("descripcion")
        
        db.session.commit()
        flash("Categoria actualizada exitosamente", "success")
        return redirect(url_for("categorias.index"))

    return render_template("categorias/edit.html", categoria=categoria)

@categorias_bp.route("/destroy/<int:id>")
@login_required
@admin_required
@referrer_required
def destroy(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    
    flash("Categoria eliminada exitosamente", "success")
    return redirect(url_for("categorias.index"))