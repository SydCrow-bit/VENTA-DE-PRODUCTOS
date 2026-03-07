from flask_login import current_user
from flask import abort, request, redirect, url_for, abort
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if current_user.role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper

def referrer_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        referrer = request.referrer
        # Obtenemos el host actual (ej: 127.0.0.1:5000)
        host = request.host 

        # EXPLICACIÓN DE LA LÓGICA:
        # 1. Si no hay referrer (escribió la URL a mano) -> Bloquear
        # 2. Si el host de nuestro sitio NO está en el referrer -> Bloquear
        if not referrer or host not in referrer:
            return redirect(url_for('auth.login'))
            
        return view_func(*args, **kwargs)
    return wrapper