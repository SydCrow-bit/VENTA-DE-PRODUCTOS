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
        # Si el usuario entra directamente, referrer es None
        # O si no viene de una ruta permitida (aquí configuramos 'login')
        if not request.referrer or "login" not in request.referrer:
            # Puedes redirigir al login o lanzar un error 403
            return redirect(url_for('auth.login'))
            
        return view_func(*args, **kwargs)
    return wrapper