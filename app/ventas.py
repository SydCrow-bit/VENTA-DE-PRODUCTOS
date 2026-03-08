from flask import Blueprint, render_template, request, jsonify, make_response
from flask_login import login_required, current_user
from fpdf import FPDF
from .extensions import db
from .models import Product, Venta, DetalleVenta, User

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
    # Retornamos el ID de la venta para que JS pueda abrir el PDF
    return jsonify({"success": True, "message": "Compra realizada con éxito", "venta_id": nueva_venta.id})
@ventas_bp.route('/recibo/<int:venta_id>')
@login_required
def recibo(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    
    if current_user.role != 'admin' and venta.user_id != current_user.id:
        return "Acceso denegado", 403

    class FacturaPDF(FPDF):
        def header(self):
            # Título de la Factura (Alineado a la derecha)
            self.set_y(10)
            self.set_font('helvetica', 'B', 24)
            self.set_text_color(59, 130, 246) # Azul primario
            self.cell(0, 10, 'FACTURA', ln=False, align='R')
            
            # Datos de la Empresa (Alineados a la izquierda)
            self.set_y(15)
            self.set_font('helvetica', 'B', 16)
            self.set_text_color(30, 41, 59) # Gris oscuro
            self.cell(0, 8, 'Venta Electrónicos S.R.L.', ln=True, align='L')
            
            self.set_font('helvetica', '', 9)
            self.set_text_color(100, 116, 139) # Gris medio
            self.cell(0, 5, 'Av. Principal #123, Zona Central', ln=True, align='L')
            self.cell(0, 5, 'Teléfono: +591 70000000 | Email: ventas@electronicos.com', ln=True, align='L')
            self.cell(0, 5, 'NIT: 1029384756', ln=True, align='L')
            
            self.ln(5)
            # Línea separadora superior
            self.set_draw_color(226, 232, 240)
            self.line(10, 40, 200, 40)
            self.ln(5)

        def footer(self):
            # Línea separadora inferior
            self.set_y(-25)
            self.set_draw_color(226, 232, 240)
            self.line(10, 272, 200, 272)
            
            # Textos del pie de página
            self.set_font('helvetica', 'B', 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 5, 'GRACIAS POR SU PREFERENCIA', ln=True, align='C')
            self.set_font('helvetica', '', 8)
            self.cell(0, 4, 'Este documento es una representación impresa de la transacción.', ln=True, align='C')
            self.cell(0, 4, f'Página {self.page_no()}', align='C')

    pdf = FacturaPDF()
    pdf.add_page()
    
    # Bloque 1: Datos del Cliente y de la Factura (2 Columnas)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(110, 6, 'DATOS DEL CLIENTE:', ln=0)
    pdf.cell(80, 6, 'DETALLES DE LA COMPRA:', ln=1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(110, 6, f'Cliente: {venta.usuario.username}', ln=0)
    pdf.cell(80, 6, f'No. Pedido: {venta.id:06d}', ln=1) # Formatea a 000001
    
    pdf.cell(110, 6, 'Moneda: Bolivianos (Bs.)', ln=0)
    pdf.cell(80, 6, f'Fecha: {venta.fecha.strftime("%d-%m-%Y %H:%M")}', ln=1)
    
    pdf.ln(10)
    
    # Bloque 2: Cabecera de la Tabla
    pdf.set_fill_color(59, 130, 246) # Fondo azul
    pdf.set_text_color(255, 255, 255) # Texto blanco
    pdf.set_draw_color(59, 130, 246) # Borde azul
    pdf.set_font('helvetica', 'B', 10)
    
    pdf.cell(90, 10, '  Descripción del Producto', border=1, align='L', fill=True)
    pdf.cell(30, 10, 'Cantidad', border=1, align='C', fill=True)
    pdf.cell(35, 10, 'P. Unitario', border=1, align='C', fill=True)
    pdf.cell(35, 10, 'Subtotal', border=1, align='C', fill=True)
    pdf.ln(10)
    
    # Bloque 3: Cuerpo de la Tabla (con colores intercalados)
    pdf.set_text_color(30, 41, 59)
    pdf.set_draw_color(226, 232, 240) # Borde gris claro
    pdf.set_font('helvetica', '', 10)
    
    # Configurar color de relleno intercalado
    pdf.set_fill_color(248, 250, 252) 
    fill = False # Variable para alternar el fondo
    
    for detalle in venta.detalles:
        subtotal = detalle.cantidad * detalle.precio_unitario
        pdf.cell(90, 10, f"  {detalle.producto.nombre}", border='LRB', align='L', fill=fill)
        pdf.cell(30, 10, str(detalle.cantidad), border='LRB', align='C', fill=fill)
        pdf.cell(35, 10, f"{detalle.precio_unitario:.2f} Bs.", border='LRB', align='R', fill=fill)
        pdf.cell(35, 10, f"{subtotal:.2f} Bs.", border='LRB', align='R', fill=fill)
        pdf.ln(10)
        fill = not fill # Invierte el valor para la siguiente fila
        
    # Bloque 4: Total y Notas
    pdf.ln(5)
    
    # Columna izquierda: Notas
    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(120, 10, ' Nota: Los productos electrónicos cuentan con 1 año de garantía.', align='L')
    
    # Columna derecha: Total resaltado
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_fill_color(59, 130, 246)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(35, 10, 'TOTAL:', align='R', fill=True)
    pdf.cell(35, 10, f"{venta.total:.2f} Bs.", align='R', fill=True)
    
    # Respuesta para el navegador
    response = make_response(bytes(pdf.output()))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=factura_{venta.id:06d}.pdf'
    
    return response

@ventas_bp.route('/historial')
@login_required
def historial():
    pedido_id = request.args.get('pedido_id', '')
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    comprador = request.args.get('comprador', '')

    query = Venta.query.join(User)

    if current_user.role != 'admin':
        query = query.filter(Venta.user_id == current_user.id)
    elif comprador:
        query = query.filter(User.username.ilike(f"%{comprador}%"))

    if pedido_id.isdigit():
        query = query.filter(Venta.id == int(pedido_id))
    
    if fecha_inicio:
        query = query.filter(Venta.fecha >= f"{fecha_inicio} 00:00:00")
        
    if fecha_fin:
        query = query.filter(Venta.fecha <= f"{fecha_fin} 23:59:59")

    ventas = query.order_by(Venta.fecha.desc()).all()
    
    filtros = {
        'pedido_id': pedido_id,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'comprador': comprador
    }
        
    return render_template('ventas/historial.html', ventas=ventas, filtros=filtros)