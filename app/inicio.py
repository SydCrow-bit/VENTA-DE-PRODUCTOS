from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from .models import User, Product, Venta, DetalleVenta
from .decorators import referrer_required
from .extensions import db

inicio_bp = Blueprint("inicio", __name__)

@inicio_bp.route("/inicio")
@login_required
@referrer_required
def inicio():
    rol = current_user.role
    datos = {}

    if rol == 'admin':
        datos['total_ventas'] = db.session.query(func.sum(Venta.total)).scalar() or 0.0
        datos['total_pedidos'] = Venta.query.count()
        datos['total_productos'] = Product.query.count()
        datos['total_usuarios'] = User.query.count()

        top_productos = db.session.query(
            Product.nombre, 
            func.sum(DetalleVenta.cantidad).label('total_vendido')
        ).join(DetalleVenta).group_by(Product.id).order_by(func.sum(DetalleVenta.cantidad).desc()).limit(5).all()

        datos['top_nombres'] = [p.nombre for p in top_productos]
        datos['top_cantidades'] = [int(p.total_vendido) for p in top_productos]

        hoy = datetime.utcnow()
        fechas_chart = []
        totales_chart = []
        
        for i in range(6, -1, -1):
            dia = hoy - timedelta(days=i)
            inicio_dia = dia.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_dia = dia.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            total_dia = db.session.query(func.sum(Venta.total)).filter(
                Venta.fecha >= inicio_dia,
                Venta.fecha <= fin_dia
            ).scalar() or 0.0
            
            fechas_chart.append(dia.strftime('%d/%m'))
            totales_chart.append(float(total_dia))

        datos['fechas_chart'] = fechas_chart
        datos['totales_chart'] = totales_chart

    else:
        datos['total_gastado'] = db.session.query(func.sum(Venta.total)).filter(Venta.user_id == current_user.id).scalar() or 0.0
        datos['mis_pedidos'] = Venta.query.filter_by(user_id=current_user.id).count()
        datos['compras_recientes'] = Venta.query.filter_by(user_id=current_user.id).order_by(Venta.fecha.desc()).limit(5).all()

    return render_template("inicio/inicio.html", rol=rol, datos=datos)