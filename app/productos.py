from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import Producto, Categoria
from .extensions import db
from .decorators import admin_required, referrer_required

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")

@productos_bp.route("/")
@login_required
@referrer_required
def index():
    productos = Producto.query.all()
    return render_template("productos/index.html", productos=productos)

@productos_bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required
def create():
    categorias = Categoria.query.all()
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        categoria_id = request.form.get("categoria_id")
        
        nuevo_producto = Producto(
            nombre=nombre, 
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        
        flash("Producto creado exitosamente", "success")
        return redirect(url_for("productos.index"))

    return render_template("productos/create.html", categorias=categorias)

@productos_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@referrer_required
def edit(id):
    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()
    
    if request.method == "POST":
        producto.nombre = request.form.get("nombre")
        producto.descripcion = request.form.get("descripcion")
        producto.precio = request.form.get("precio")
        producto.stock = request.form.get("stock")
        producto.categoria_id = request.form.get("categoria_id")
        
        db.session.commit()
        flash("Producto actualizado exitosamente", "success")
        return redirect(url_for("productos.index"))

    return render_template("productos/edit.html", producto=producto, categorias=categorias)

@productos_bp.route("/destroy/<int:id>")
@login_required
@admin_required
@referrer_required
def destroy(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    
    flash("Producto eliminado exitosamente", "success")
    return redirect(url_for("productos.index"))