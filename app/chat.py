import os
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from google import genai
from google.genai import types

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

GEMINI_API_KEY = "api_key"
GEMINI_MODEL = "gemini-3-flash-preview"

client = genai.Client(api_key=GEMINI_API_KEY)

@chat_bp.route('/', methods=['POST'])
@login_required
def generate_chat_response():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    history = data.get('history', [])

    if not user_message:
        return jsonify({'error': 'Mensaje vacío'}), 400

    rol_usuario = "Administrador (puede gestionar inventario, ver ventas globales y usuarios)" if current_user.role == 'admin' else "Cliente (puede explorar el catálogo, agregar al carrito y comprar)"
    
    system_instruction = f"""Eres 'Beaver', el asistente virtual experto y amable del sistema de Punto de Venta (POS) e Inventario de 'Venta Electrónicos S.R.L.'.
    Estás interactuando con el usuario: {current_user.username}.
    Su rol en el sistema es: {rol_usuario}.
    
    Tus objetivos:
    1. Ayudar a resolver dudas sobre cómo usar el sistema (compras, inventario, facturación en PDF).
    2. Dar recomendaciones de productos electrónicos si te lo piden.
    3. Mantener un tono profesional, servicial y conciso.
    4. Nunca inventes datos de stock o precios si no los conoces, sugiere que revisen el catálogo.
    5. Responde en texto plano o usando formato muy básico. Sé directo para no hacer al usuario leer demasiado."""

    conversation_context = ""
    if history:
        conversation_context = "Historial reciente:\n"
        for msg in history[-6:]:
            sender = "Usuario" if msg['role'] == 'user' else "Beaver"
            conversation_context += f"{sender}: {msg['text']}\n"

    full_prompt = f"{conversation_context}\nUsuario: {user_message}\nBeaver:"

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6,
                max_output_tokens=500
            )
        )
        return jsonify({'response': response.text.strip()})
    except Exception as e:
        print(f"Error de Gemini: {e}")
        return jsonify({'error': 'Ocurrió un error al conectar con el cerebro de Beaver. Intenta de nuevo más tarde.'}), 500