from .extensions import login_manager
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# CODIGO AGREGADO 

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# --- CRUD DE CATEGORÍAS ---

@app.route('/admin/categorias')
@login_required
def lista_categorias():
    if current_user.role != 'admin': # Validación de rol obligatoria
        return "Acceso denegado", 403
    
    # Leer con filtro/búsqueda (Requisito del examen)
    busqueda = request.args.get('search', '')
    if busqueda:
        categorias = Category.query.filter(Category.nombre.contains(busqueda)).all()
    else:
        categorias = Category.query.all()
    
    return render_template('admin/lista_categorias.html', categorias=categorias, busqueda=busqueda)

@app.route('/admin/categorias/crear', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    if current_user.role != 'admin':
        return "Acceso denegado", 403

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # Validación simple (Requisito del examen)
        if not nombre:
            flash('El nombre es obligatorio')
        else:
            nueva_cat = Category(nombre=nombre)
            db.session.add(nueva_cat)
            db.session.commit()
            return redirect(url_for('lista_categorias'))
            
    return render_template('admin/crear_categoria.html')

        # EDITAR Y ELIMINAR (SOLO ADMIN)
# --- CONTINUACIÓN CRUD DE CATEGORÍAS ---

@app.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
    
    categoria = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # Validación de campo obligatorio
        if not nombre:
            flash('El nombre de la categoría no puede estar vacío.', 'danger')
        else:
            categoria.nombre = nombre
            db.session.commit()
            flash('Categoría actualizada correctamente.', 'success')
            return redirect(url_for('lista_categorias'))
            
    return render_template('admin/editar_categoria.html', categoria=categoria)

@app.route('/admin/categorias/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_categoria(id):
    if current_user.role != 'admin':
        return "Acceso denegado", 403
        
    categoria = Category.query.get_or_404(id)
    try:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada con éxito.', 'success')
    except:
        # Validación: Evita eliminar si tiene productos asociados (integridad referencial)
        flash('No se puede eliminar la categoría porque tiene productos vinculados.', 'danger')
        
    return redirect(url_for('lista_categorias'))
