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