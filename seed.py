import random
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Category, Product, Venta, DetalleVenta

app = create_app()

def seed_database():
    with app.app_context():
        DetalleVenta.query.delete()
        Venta.query.delete()
        Product.query.delete()
        Category.query.delete()
        User.query.delete()
        db.session.commit()

        users_data = [
            {"username": "admin", "password": "password123", "role": "admin"},
            {"username": "carlos_cliente", "password": "password123", "role": "user"},
            {"username": "maria_tech", "password": "password123", "role": "user"},
            {"username": "juan_gamer", "password": "password123", "role": "user"},
            {"username": "ana_dev", "password": "password123", "role": "user"},
            {"username": "luis_compras", "password": "password123", "role": "user"}
        ]

        users = []
        for data in users_data:
            new_user = User(username=data["username"], role=data["role"])
            new_user.set_password(data["password"])
            db.session.add(new_user)
            users.append(new_user)
        
        db.session.commit()

        categories_data = ["Laptops", "Smartphones", "Audio", "Accesorios", "Televisores", "Monitores"]
        category_map = {}

        for cat_name in categories_data:
            category = Category(nombre=cat_name)
            db.session.add(category)
            db.session.commit()
            category_map[cat_name] = category.id

        products_data = [
            {"nombre": "Apple MacBook Pro 14\"", "descripcion": "Chip M3 Pro, 18GB RAM, 512GB SSD.", "precio": 1999.99, "stock": 60, "cat": "Laptops", "img": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?q=80&w=800"},
            {"nombre": "Dell XPS 15", "descripcion": "Intel Core i7, 16GB RAM, 1TB SSD, RTX 4050.", "precio": 1499.00, "stock": 45, "cat": "Laptops", "img": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?q=80&w=800"},
            {"nombre": "iPhone 15 Pro", "descripcion": "Apple A17 Pro, 256GB, Titanio Natural.", "precio": 1099.00, "stock": 80, "cat": "Smartphones", "img": "https://cdsassets.apple.com/live/7WUAS350/images/tech-specs/iphone_15_pro.png"},
            {"nombre": "Samsung Galaxy S24 Ultra", "descripcion": "Snapdragon 8 Gen 3, 512GB, IA integrada.", "precio": 1299.99, "stock": 70, "cat": "Smartphones", "img": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?q=80&w=800"},
            {"nombre": "Sony WH-1000XM5", "descripcion": "Auriculares inalámbricos con cancelación de ruido activa.", "precio": 398.00, "stock": 90, "cat": "Audio", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800"},
            {"nombre": "Apple AirPods Pro 2", "descripcion": "Auriculares in-ear con USB-C y cancelación de ruido.", "precio": 249.00, "stock": 120, "cat": "Audio", "img": "https://tecnopolis.com.bo/cdn/shop/files/airp-2.png?crop=center&height=900&v=1757016376&width=720"},
            {"nombre": "Logitech MX Master 3S", "descripcion": "Ratón inalámbrico ergonómico, sensor 8K DPI.", "precio": 99.99, "stock": 85, "cat": "Accesorios", "img": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=800"},
            {"nombre": "Keychron K2", "descripcion": "Teclado mecánico inalámbrico formato 75%.", "precio": 79.00, "stock": 65, "cat": "Accesorios", "img": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?q=80&w=800"},
            {"nombre": "LG OLED C3 55\"", "descripcion": "Smart TV 4K, 120Hz, ideal para gaming.", "precio": 1296.00, "stock": 30, "cat": "Televisores", "img": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?q=80&w=800"},
            {"nombre": "Monitor Dell UltraSharp 27\"", "descripcion": "Monitor 4K USB-C Hub ideal para productividad.", "precio": 550.00, "stock": 40, "cat": "Monitores", "img": "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?q=80&w=800"}
        ]

        productos_db = []
        for prod_data in products_data:
            product = Product(
                nombre=prod_data["nombre"],
                descripcion=prod_data["descripcion"],
                precio=prod_data["precio"],
                stock=prod_data["stock"],
                imagen=prod_data["img"],
                category_id=category_map[prod_data["cat"]]
            )
            db.session.add(product)
            productos_db.append(product)
        
        db.session.commit()

        clientes = [u for u in users if u.role == 'user']
        hoy = datetime.utcnow()

        for _ in range(60):
            cliente = random.choice(clientes)
            dias_atras = random.randint(0, 6)
            horas_atras = random.randint(0, 23)
            minutos_atras = random.randint(0, 59)
            fecha_venta = hoy - timedelta(days=dias_atras, hours=horas_atras, minutes=minutos_atras)

            nueva_venta = Venta(user_id=cliente.id, fecha=fecha_venta, total=0.0)
            db.session.add(nueva_venta)
            db.session.flush()

            num_items = random.randint(1, 3)
            productos_seleccionados = random.sample(productos_db, num_items)
            
            total_venta = 0.0
            
            for prod in productos_seleccionados:
                cantidad = random.randint(1, 2)
                precio_unitario = prod.precio
                
                if prod.stock >= cantidad:
                    detalle = DetalleVenta(
                        venta_id=nueva_venta.id,
                        product_id=prod.id,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario
                    )
                    prod.stock -= cantidad
                    total_venta += (cantidad * precio_unitario)
                    db.session.add(detalle)
            
            nueva_venta.total = total_venta
        
        db.session.commit()
        print("Seeding completado.")

if __name__ == "__main__":
    seed_database()