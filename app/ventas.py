from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .extensions import db
from .models import Product, Venta, DetalleVenta

ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@ventas_bp.route('/catalogo')
@login_required
def catalogo():
    productos = Product.query.filter(Product.stock > 0).all()
    return render_template('ventas/catalogo.html', productos=productos)

@ventas_bp.route('/carrito')
@login_required
def carrito():
    return render_template('ventas/carrito.html')

@ventas_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    datos = request.get_json()
    
    if not datos or len(datos) == 0:
        return jsonify({"success": False, "message": "El carrito está vacío"}), 400

    total_venta = sum(item['precio'] * item['cantidad'] for item in datos)

    nueva_venta = Venta(user_id=current_user.id, total=total_venta)
    db.session.add(nueva_venta)
    db.session.flush()

    for item in datos:
        producto = Product.query.get(item['product_id'])
        if producto and producto.stock >= item['cantidad']:
            detalle = DetalleVenta(
                venta_id=nueva_venta.id,
                product_id=producto.id,
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            )
            producto.stock -= item['cantidad']
            db.session.add(detalle)
        else:
            db.session.rollback()
            return jsonify({"success": False, "message": f"Stock insuficiente para el producto ID {item['product_id']}"}), 400

    db.session.commit()
    return jsonify({"success": True, "message": "Compra realizada con éxito"})

@ventas_bp.route('/historial')
@login_required
def historial():
    if current_user.role == 'admin':
        ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    else:
        ventas = Venta.query.filter_by(user_id=current_user.id).order_by(Venta.fecha.desc()).all()
        
    return render_template('ventas/historial.html', ventas=ventas)