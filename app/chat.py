import os
import traceback
import logging
from .extensions import db
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_
from google import genai
from google.genai import types
from app.models import Product, Category, Venta, DetalleVenta
from config import Config


# --- CONFIGURACIÓN DE LOGS ---
# force=True obliga a Flask a escribir en este archivo en lugar de la consola
logging.basicConfig(
    filename='chatbot_debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    force=True 
)

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-3-flash",
    "gemini-2.5-flash-lite"
]

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def call_gemini_with_fallback(contents, config):
    last_error = None
    for model in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            return response
        except Exception as e:
            err_str = str(e)
            print(f"Fallo con {model} -> {err_str}")
            last_error = e
            if "429" in err_str or "404" in err_str or "quota" in err_str.lower():
                continue
            else:
                raise e
    raise Exception(f"Todos los modelos fallaron. Último error: {str(last_error)}")

@chat_bp.route('/', methods=['POST'])
@login_required
def generate_chat_response():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    history_data = data.get('history', [])

    if not user_message:
        return jsonify({'error': 'Mensaje vacío'}), 400

    logging.info(f"Usuario: {current_user.username} | Mensaje: {user_message}")

    def buscar_inventario(termino_busqueda: str = "") -> dict:
        try:
            query = Product.query.join(Category)
            if termino_busqueda:
                query = query.filter(
                    or_(
                        Product.nombre.ilike(f'%{termino_busqueda}%'),
                        Category.nombre.ilike(f'%{termino_busqueda}%'),
                        Product.descripcion.ilike(f'%{termino_busqueda}%')
                    )
                )
            
            # Subimos el límite para que la IA vea más catálogo al armar una PC
            productos = query.limit(30).all()
            
            if not productos:
                return {"mensaje": f"No se encontraron componentes para '{termino_busqueda}'."}
                
            resultados = []
            for p in productos:
                resultados.append({
                    "nombre": p.nombre,
                    "precio_usd": float(p.precio),
                    "stock": p.stock,
                    "categoria": p.category.nombre
                })
            return {"productos": resultados}
        except Exception as e:
            return {"error": f"Error al buscar en inventario: {str(e)}"}

    def resumen_mis_compras(solicitar: bool = True) -> dict:
        try:
            ventas = Venta.query.filter_by(user_id=current_user.id).order_by(Venta.fecha.desc()).limit(5).all()
            if not ventas:
                return {"mensaje": "El usuario no ha realizado ninguna compra todavía."}
            
            resultados = []
            for v in ventas:
                detalles_db = DetalleVenta.query.filter_by(venta_id=v.id).all()
                lista_detalles = []
                for d in detalles_db:
                    prod = Product.query.get(d.product_id)
                    nombre_prod = prod.nombre if prod else "Componente desconocido"
                    lista_detalles.append({
                        "producto": nombre_prod, 
                        "cantidad": d.cantidad, 
                        "precio_unitario_usd": float(d.precio_unitario)
                    })
                
                resultados.append({
                    "id_venta": v.id,
                    "fecha": v.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    "total_gastado_usd": float(v.total),
                    "articulos": lista_detalles
                })
            return {"ultimas_compras": resultados}
        except Exception as e:
            return {"error": f"Error de base de datos al leer compras: {str(e)}"}
        
    #METODOS PARA CHATBOT PARA ADMIS
    def ventas_hoy() -> dict:
        try:

            from datetime import date

            ventas = Venta.query.filter(
                Venta.fecha >= date.today()
            ).all()

            total = sum(v.total for v in ventas)

            return {
                "ventas_hoy": len(ventas),
                "ingresos": float(total)
            }

        except Exception as e:
            return {"error":str(e)}
    
    def productos_bajo_stock() -> dict:
        try:

            productos = Product.query.filter(
                Product.stock <= 5
            ).all()

            if not productos:
                return {"mensaje":"No hay productos con bajo stock"}

            data=[]

            for p in productos:

                data.append({
                    "nombre":p.nombre,
                    "stock":p.stock
                })

            return {"productos_bajo_stock":data}

        except Exception as e:
            return {"error":str(e)}
    def productos_mas_vendidos():
        try:
            from sqlalchemy import func

            result = db.session.query(
                DetalleVenta.product_id,
                func.sum(DetalleVenta.cantidad)
            ).group_by(
                DetalleVenta.product_id
            ).order_by(
                func.sum(DetalleVenta.cantidad).desc()
            ).limit(5).all()

            data=[]

            for r in result:

                product = Product.query.get(r[0])

                data.append({
                    "producto":product.nombre,
                    "cantidad":int(r[1])
                })

            return {"top_productos":data}

        except Exception as e:
            return {"error":str(e)}
    def generar_link_compra(productos_cotizados: list[str]) -> dict:
        """
        Llama a esta herramienta cuando el usuario acepte una cotización para generarle el link de compra.
        'productos_cotizados' debe ser una lista de nombres de los productos exactos, ej: ["Ryzen 5 5600G", "Memoria RAM 8GB"]
        """
        try:
            items_link = []
            for nombre in productos_cotizados:
                # Buscamos el producto en la BD por su nombre
                prod = Product.query.filter(Product.nombre.ilike(f"%{nombre}%")).first()
                if prod:
                    # Asumimos cantidad 1 por defecto para simplificar
                    items_link.append(f"{prod.id}-1")
            
            if not items_link:
                return {"mensaje": "No pude generar el link porque no encontré los IDs exactos."}
                
            param = ",".join(items_link)
            link_markdown = f"[¡Haz clic aquí para añadir esta cotización a tu carrito!](/ventas/carrito?add={param})"
            return {"link_generado": link_markdown}
        except Exception as e:
            return {"error": f"Error al generar link: {str(e)}"}
        
    rol_usuario = "Administrador" if current_user.role == 'admin' else "Cliente"
    
    system_instruction = f"""Eres 'Beaver', experto en hardware de 'Venta Electronicos S.R.L.'.
    Usuario: {current_user.username} (Rol: {rol_usuario}).
    
    REGLAS ESTRICTAS:
    1. Precios en Bolivianos (Bs). NO conviertas a dolares.
    2. Para armar PC o presupuesto, llama a 'buscar_inventario' con "".
    3. Verifica compatibilidad estrictamente.
    4. Presupuestos bajos (4000-5000 Bs): sugiere procesadores con graficos integrados.
    5. Usa solo stock y precios de la base de datos.
    6. Se directo, profesional y muy conciso. Usa vinetas. Evita textos largos para ahorrar tokens.
    7. Actua como un cajero cerrando la venta. Tras dar la cotizacion, pregunta de forma directa si desea proceder con la compra.
    8. Si el usuario acepta comprar, LLAMA a 'generar_link_compra' con la lista de nombres de los productos. Muestra el enlace generado al usuario."""

    formatted_history = []
    for msg in history_data[-6:]:
        role = "user" if msg['role'] == 'user' else "model"
        formatted_history.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg['text'])])
        )

    contents = formatted_history + [types.Content(role="user", parts=[types.Part.from_text(text=user_message)])]
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        max_output_tokens=2048, # AUMENTADO para que no se corten los presupuestos largos
        tools=[buscar_inventario, resumen_mis_compras, ventas_hoy, productos_bajo_stock, productos_mas_vendidos, generar_link_compra]
    )

    try:
        response = call_gemini_with_fallback(contents, config)
        
        texto_final = response.text.strip()
        
        logging.info(f"Respuesta final IA: \n{texto_final}\n{'-'*40}")
        
        return jsonify({'response': texto_final})

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error CRÍTICO:\n{error_details}")
        
        logging.error(f"Error CRÍTICO procesando el chat: {error_details}\n{'-'*40}")
        
        mensaje_error = str(e).replace("API key not valid", "Tu API Key no es válida o faltó reemplazarla.")
        return jsonify({'error': f'Detalle del error: {mensaje_error}'}), 500