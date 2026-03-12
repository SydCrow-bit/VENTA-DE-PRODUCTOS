from flask import Blueprint, jsonify
from flask_login import login_required

from google import genai
from google.genai import types

from sqlalchemy import func

from app.models import Product, Venta, DetalleVenta
from app.extensions import db
from config import Config

from datetime import datetime


ai_dashboard_bp = Blueprint(

    "ai_dashboard",

    __name__,

    url_prefix="/api/ai"

)


client = genai.Client(

    api_key=Config.GEMINI_API_KEY

)


# ==========================
# OBTENER DATOS DEL NEGOCIO
# ==========================

def obtener_datos_negocio():

    total = db.session.query(

        func.sum(Venta.total)

    ).scalar() or 0


    ventas = Venta.query.count()


    productos = Product.query.count()


    ticket = 0

    if ventas > 0:

        ticket = total / ventas


    top = db.session.query(

        Product.nombre,

        func.sum(DetalleVenta.cantidad)

    ).join(

        DetalleVenta

    ).group_by(

        Product.id

    ).order_by(

        func.sum(
            DetalleVenta.cantidad
        ).desc()

    ).limit(5).all()


    lista_top=[]


    for p in top:

        lista_top.append(

            f"{p[0]} ({int(p[1])} ventas)"

        )


    if not lista_top:

        lista_top.append(

            "Sin datos suficientes"
        )


    return {

        "total":round(total,2),

        "ventas":ventas,

        "productos":productos,

        "ticket":round(ticket,2),

        "top":lista_top

    }


# ==========================
# ANALISIS IA NEGOCIO
# ==========================

import re

def limpiar_markdown(texto):

    texto = re.sub(r'\*+', '', texto)

    texto = re.sub(r'\#+', '', texto)

    texto = re.sub(r'\-+', '', texto)

    return texto



def generar_analisis_negocio(datos):

    prompt=f"""
Datos del sistema:

Ingresos: {datos["total"]} Bs
Ventas: {datos["ventas"]}
Productos: {datos["productos"]}
Ticket promedio: {datos["ticket"]}

Top productos:
{",".join(datos["top"])}

Genera un análisis comercial completo.

Mínimo 5 párrafos.

Solo texto normal.

No uses:

#
*
**
listas
markdown
títulos

Solo análisis en texto plano.
"""


    config = types.GenerateContentConfig(

        temperature=0.7,

        max_output_tokens=1800,

        top_p=0.9

    )


    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt,

        config=config

    )


    try:

        texto=""

        for part in response.candidates[0].content.parts:

            if hasattr(part,"text"):

                texto+=part.text


        return limpiar_markdown(texto)

    except:

        return "Error generando análisis"

# ==========================
# ROUTE ANALISIS NEGOCIO
# ==========================

@ai_dashboard_bp.route(

"/analysis"

)

@login_required
def ai_analysis():

    try:

        datos = obtener_datos_negocio()

        analysis = generar_analisis_negocio(datos)

        return jsonify({

            "status":"success",

            "analysis":analysis,

            "generated":datetime.now().strftime("%H:%M")

        })


    except Exception as e:

        return jsonify({

            "status":"error",

            "message":str(e)

        }),500
# ==========================
# RIESGO INVENTARIO
# ==========================

def obtener_riesgo_inventario():
    productos = Product.query.all()
    resultados = []

    for p in productos:
        # Si el stock es menor a 5 unidades, consideramos riesgo alto
        riesgo = "Bajo"
        if p.stock <= 5:
            riesgo = "Alto"
        elif p.stock <= 10:
            riesgo = "Medio"

        resultados.append(f"{p.nombre}: Stock {p.stock} unidades - Riesgo {riesgo}")

    if not resultados:
        resultados.append("No hay productos registrados")

    return resultados


def generar_riesgo_inventario(datos):
    prompt = f"""
Estos son los productos y su stock:
{', '.join(datos)}

Genera un análisis sobre los riesgos de inventario.
Indica productos críticos y posibles acciones para mitigarlos.
Escribe mínimo 3 párrafos, solo texto plano, sin markdown ni listas.
"""

    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=1200,
        top_p=0.9
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    try:
        texto = ""
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text"):
                texto += part.text
        return limpiar_markdown(texto)
    except:
        return "Error generando análisis de inventario"

@ai_dashboard_bp.route("/stock")
@login_required
def ai_stock():
    try:
        datos = obtener_riesgo_inventario()
        analysis = generar_riesgo_inventario(datos)
        return jsonify({
            "status": "success",
            "analysis": analysis,
            "generated": datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
# ==========================
# INSIGHTS VENTAS
# ==========================

def obtener_datos_ventas():
    total_ventas = db.session.query(func.sum(Venta.total)).scalar() or 0
    num_ventas = Venta.query.count()
    ticket = round(total_ventas / num_ventas, 2) if num_ventas > 0 else 0

    top_productos = db.session.query(
        Product.nombre,
        func.sum(DetalleVenta.cantidad)
    ).join(DetalleVenta).group_by(Product.id).order_by(
        func.sum(DetalleVenta.cantidad).desc()
    ).limit(5).all()

    lista_top = [f"{p[0]} ({int(p[1])} ventas)" for p in top_productos] or ["Sin datos suficientes"]

    return {
        "total_ventas": round(total_ventas, 2),
        "num_ventas": num_ventas,
        "ticket_promedio": ticket,
        "top_productos": lista_top
    }


def generar_insights_ventas(datos):
    prompt = f"""
Datos de ventas:
Ingresos totales: {datos['total_ventas']} Bs
Número de ventas: {datos['num_ventas']}
Ticket promedio: {datos['ticket_promedio']}
Top productos: {', '.join(datos['top_productos'])}

Genera insights sobre ventas: tendencias, oportunidades de crecimiento, y estrategias recomendadas.
Mínimo 4 párrafos, solo texto plano, sin markdown ni listas.
"""

    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=1500,
        top_p=0.9
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config
    )

    try:
        texto = ""
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text"):
                texto += part.text
        return limpiar_markdown(texto)
    except:
        return "Error generando insights de ventas"


@ai_dashboard_bp.route("/sales")
@login_required
def ai_sales():
    try:
        datos = obtener_datos_ventas()
        analysis = generar_insights_ventas(datos)
        return jsonify({
            "status": "success",
            "analysis": analysis,
            "generated": datetime.now().strftime("%H:%M")
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500