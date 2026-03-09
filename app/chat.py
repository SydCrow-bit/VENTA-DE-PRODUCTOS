import os
import traceback
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_
from google import genai
from google.genai import types
from app.models import Product, Category, Venta, DetalleVenta

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

GEMINI_API_KEY = "api_key"

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-3-flash",
    "gemini-2.5-flash-lite"
]

client = genai.Client(api_key=GEMINI_API_KEY)

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

    rol_usuario = "Administrador" if current_user.role == 'admin' else "Cliente"
    
    system_instruction = f"""Eres 'Beaver', el experto en hardware de PC de 'Venta Electrónicos S.R.L.'.
    Tu especialidad es armar presupuestos de computadoras verificando compatibilidades y buscando piezas en el inventario.
    Estás interactuando con: {current_user.username} (Rol: {rol_usuario}).
    
    REGLAS ESTRICTAS:
    1. IMPORTANTE SOBRE LA MONEDA: Todos los precios en la base de datos están en Bolivianos (Bs). NO hagas conversiones a dólares. 
    2. SIEMPRE que te pidan armar una PC o presupuesto, llama a la herramienta 'buscar_inventario' enviando "".
    3. Verifica compatibilidad (ej. procesador AMD con placa base AM4 o AM5 según corresponda, y DDR4 vs DDR5).
    4. Si un usuario tiene poco presupuesto (ej. 4000 Bs - 5000 Bs), aconséjale usar procesadores con gráficos integrados (ej. Ryzen 5600G o 5700G) para ahorrar el costo de la tarjeta de video dedicada.
    5. No inventes stock ni precios, solo usa la información de la base de datos.
    6. Sé profesional, amigable y usa formato de viñetas para listar los componentes cotizados, mostrando el costo final de la PC."""

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
        max_output_tokens=800,
        tools=[buscar_inventario, resumen_mis_compras]
    )

    try:
        response = call_gemini_with_fallback(contents, config)

        if response.function_calls:
            contents.append(response.candidates[0].content)
            
            function_response_parts = []
            for function_call in response.function_calls:
                name = function_call.name
                args = dict(function_call.args) if function_call.args else {}
                
                if name == "buscar_inventario":
                    res = buscar_inventario(args.get("termino_busqueda", ""))
                elif name == "resumen_mis_compras":
                    res = resumen_mis_compras(args.get("solicitar", True))
                else:
                    res = {"error": "Función desconocida."}
                    
                function_response_parts.append(
                    types.Part.from_function_response(
                        name=name,
                        response=res
                    )
                )
                
            contents.append(types.Content(role="user", parts=function_response_parts))
            
            final_response = call_gemini_with_fallback(contents, config)
            return jsonify({'response': final_response.text.strip()})
        
        return jsonify({'response': response.text.strip()})

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error CRÍTICO:\n{error_details}")
        mensaje_error = str(e).replace("API key not valid", "Tu API Key no es válida o faltó reemplazarla.")
        return jsonify({'error': f'Detalle del error: {mensaje_error}'}), 500