from flask import Flask
from .extensions import db, login_manager, migrate
from config import Config
from .models import User

def create_app():
    app = Flask(__name__)

    # cargar configuracion
    app.config.from_object(Config)

    # inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # importar blueprints
    from .auth import auth_bp
    from .admin import admin_bp
    from .inicio import inicio_bp
    from .routes import routes_bp
    from .ventas import ventas_bp
    from .chat import chat_bp

    # registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(inicio_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(chat_bp)
    return app