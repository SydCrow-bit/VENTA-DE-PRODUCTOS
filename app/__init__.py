from flask import Flask
from .extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__)

    # cargar configuracion
    app.config.from_object(Config)

    # inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # importar blueprints
    from .auth import auth_bp
    from .admin import admin_bp

    # registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app