from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .extensions import db, login_manager
from .models import User, Category, Product

# Definimos el Blueprint para este archivo
routes_bp = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- CRUD DE CATEGORÍAS ---

@routes_bp.route('/admin/categorias')
@login_required
def lista_categorias():
    if current_user.role != 'admin':
        return "Acceso denegado", 403
    
    busqueda = request.args.get('search', '')
    if busqueda:
        categorias = Category.query.filter(Category.nombre.contains(busqueda)).all()
    else:
        categorias = Category.query.all()
    
    return render_template('admin/lista_categorias.html', categorias=categorias, busqueda=busqueda)

@routes_bp.route('/admin/categorias/crear', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    if current_user.role != 'admin':
        return "Acceso denegado", 403

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
        else:
            nueva_cat = Category(nombre=nombre)
            db.session.add(nueva_cat)
            db.session.commit()
            flash('Categoría creada con éxito', 'success')
            return redirect(url_for('routes.lista_categorias'))
            
    return render_template('admin/crear_categoria.html')

@routes_bp.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
    
    categoria = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if not nombre:
            flash('El nombre de la categoría no puede estar vacío.', 'danger')
        else:
            categoria.nombre = nombre
            db.session.commit()
            flash('Categoría actualizada correctamente.', 'success')
            return redirect(url_for('routes.lista_categorias'))
            
    return render_template('admin/editar_categoria.html', categoria=categoria)

@routes_bp.route('/admin/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_categoria(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
        
    categoria = Category.query.get_or_404(id)
    try:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada con éxito.', 'success')
    except Exception:
        db.session.rollback()
        flash('No se puede eliminar: tiene productos vinculados.', 'danger')
        
    return redirect(url_for('routes.lista_categorias'))

# --- CRUD DE PRODUCTOS ---

@routes_bp.route('/admin/productos')
@login_required
def lista_productos():
    if current_user.role != 'admin':
        return "Acceso denegado", 403
    
    busqueda = request.args.get('search', '')
    if busqueda:
        productos = Product.query.filter(Product.nombre.contains(busqueda)).all()
    else:
        productos = Product.query.all()
    
    return render_template('admin/lista_productos.html', productos=productos, busqueda=busqueda)

@routes_bp.route('/admin/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if current_user.role != 'admin':
        return "Acceso denegado", 403

    categorias = Category.query.all()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')

        if not nombre or not precio or not category_id:
            flash('Nombre, Precio y Categoría son obligatorios', 'danger')
        else:
            try:
                nuevo_prod = Product(
                    nombre=nombre, 
                    precio=float(precio), 
                    stock=int(stock), 
                    category_id=int(category_id)
                )
                db.session.add(nuevo_prod)
                db.session.commit()
                flash('Producto creado con éxito', 'success')
                return redirect(url_for('routes.lista_productos'))
            except ValueError:
                flash('Precio o Stock inválidos', 'danger')
            
    return render_template('admin/crear_producto.html', categorias=categorias)

@routes_bp.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
    
    producto = Product.query.get_or_404(id)
    categorias = Category.query.all()
    
    if request.method == 'POST':
        try:
            producto.nombre = request.form.get('nombre')
            producto.precio = float(request.form.get('precio'))
            producto.stock = int(request.form.get('stock'))
            producto.category_id = int(request.form.get('category_id'))
            producto.descripcion = request.form.get('descripcion')

            if not producto.nombre:
                flash('El nombre es obligatorio', 'danger')
            else:
                db.session.commit()
                flash('Producto actualizado correctamente', 'success')
                return redirect(url_for('routes.lista_productos'))
        except ValueError:
            flash('Verifica que el precio y stock sean números válidos', 'danger')
            
    return render_template('admin/editar_producto.html', producto=producto, categorias=categorias)

@routes_bp.route('/admin/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
        
    producto = Product.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado', 'success')
    return redirect(url_for('routes.lista_productos'))