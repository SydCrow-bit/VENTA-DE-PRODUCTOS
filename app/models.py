from flask_login import UserMixin
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    productos = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.nombre}>'

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    imagen = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'<Product {self.nombre}>'

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    usuario = db.relationship('User', backref='ventas', lazy=True)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade="all, delete-orphan")

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    producto = db.relationship('Product', backref='detalles_venta', lazy=True)