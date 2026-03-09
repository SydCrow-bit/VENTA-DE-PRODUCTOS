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

        categories_data = [
            "Procesadores", "Tarjetas Gráficas", "Placas Base", 
            "Memoria RAM", "Almacenamiento", "Fuentes de Poder", "Gabinetes", "Monitores", "Periféricos"
        ]
        category_map = {}

        for cat_name in categories_data:
            category = Category(nombre=cat_name)
            db.session.add(category)
            db.session.commit()
            category_map[cat_name] = category.id

        # Precios estimados en Bolivianos (Bs)
        products_data = [
            # PROCESADORES (Gama de entrada, media y alta)
            {"nombre": "AMD Ryzen 5 4600G", "descripcion": "6 Núcleos, Gráficos integrados Radeon, AM4. Ideal oficina.", "precio": 750.00, "stock": 25, "cat": "Procesadores", "img": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=800"},
            {"nombre": "AMD Ryzen 5 5600G", "descripcion": "6 Núcleos, Gráficos integrados, AM4. Excelente para esports.", "precio": 1100.00, "stock": 40, "cat": "Procesadores", "img": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=800"},
            {"nombre": "AMD Ryzen 7 5700G", "descripcion": "8 Núcleos, Gráficos integrados potentes, AM4.", "precio": 1550.00, "stock": 30, "cat": "Procesadores", "img": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=800"},
            {"nombre": "Intel Core i5-12400F", "descripcion": "6 Núcleos, sin gráficos integrados, LGA 1700.", "precio": 1250.00, "stock": 20, "cat": "Procesadores", "img": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=800"},
            {"nombre": "AMD Ryzen 5 7600X", "descripcion": "6 Núcleos, AM5, DDR5. Alto rendimiento.", "precio": 1850.00, "stock": 15, "cat": "Procesadores", "img": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=800"},

            # PLACAS BASE
            {"nombre": "Biostar A320M", "descripcion": "Placa base económica AM4, 2 slots RAM DDR4.", "precio": 380.00, "stock": 50, "cat": "Placas Base", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800"},
            {"nombre": "Gigabyte B450M DS3H", "descripcion": "Placa base AM4, 4 slots RAM, excelente calidad-precio.", "precio": 650.00, "stock": 45, "cat": "Placas Base", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800"},
            {"nombre": "ASUS Prime H610M-E", "descripcion": "Placa base LGA 1700 para Intel 12va/13va gen, DDR4.", "precio": 700.00, "stock": 30, "cat": "Placas Base", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800"},
            {"nombre": "MSI B650M-P", "descripcion": "Placa base AM5 para Ryzen 7000, soporte DDR5.", "precio": 1200.00, "stock": 20, "cat": "Placas Base", "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800"},

            # MEMORIA RAM
            {"nombre": "Kingston Fury Beast 8GB DDR4", "descripcion": "Memoria RAM 3200MHz con disipador.", "precio": 180.00, "stock": 100, "cat": "Memoria RAM", "img": "https://images.unsplash.com/photo-1562976540-1502f714426d?q=80&w=800"},
            {"nombre": "Corsair Vengeance LPX 16GB (2x8GB) DDR4", "descripcion": "Kit 16GB 3200MHz, ideal para Dual Channel.", "precio": 400.00, "stock": 60, "cat": "Memoria RAM", "img": "https://images.unsplash.com/photo-1562976540-1502f714426d?q=80&w=800"},
            {"nombre": "Kingston Fury Beast 16GB DDR5", "descripcion": "Memoria RAM 5200MHz, nueva generación.", "precio": 550.00, "stock": 40, "cat": "Memoria RAM", "img": "https://images.unsplash.com/photo-1562976540-1502f714426d?q=80&w=800"},

            # ALMACENAMIENTO
            {"nombre": "Kingston A400 240GB SSD", "descripcion": "SSD SATA 2.5, ideal para sistema operativo.", "precio": 150.00, "stock": 80, "cat": "Almacenamiento", "img": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=800"},
            {"nombre": "Crucial P3 500GB NVMe", "descripcion": "SSD M.2 PCIe 3.0, alta velocidad de lectura.", "precio": 320.00, "stock": 60, "cat": "Almacenamiento", "img": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=800"},
            {"nombre": "Western Digital Blue 1TB NVMe", "descripcion": "SSD M.2 PCIe 3.0, excelente capacidad y velocidad.", "precio": 550.00, "stock": 50, "cat": "Almacenamiento", "img": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=800"},
            {"nombre": "Seagate Barracuda 1TB HDD", "descripcion": "Disco duro mecánico 7200RPM para almacenamiento masivo.", "precio": 350.00, "stock": 40, "cat": "Almacenamiento", "img": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?q=80&w=800"},

            # FUENTES DE PODER
            {"nombre": "Fuente Genérica 500W", "descripcion": "Fuente básica para equipos de oficina sin gráfica dedicada.", "precio": 120.00, "stock": 50, "cat": "Fuentes de Poder", "img": "https://images.unsplash.com/photo-1587202372616-b43abea06c2a?q=80&w=800"},
            {"nombre": "EVGA 500W 80+ White", "descripcion": "Fuente certificada, segura para setups básicos con gráfica.", "precio": 380.00, "stock": 40, "cat": "Fuentes de Poder", "img": "https://images.unsplash.com/photo-1587202372616-b43abea06c2a?q=80&w=800"},
            {"nombre": "Corsair CV650 650W 80+ Bronze", "descripcion": "Fuente confiable para gráficas de gama media/alta.", "precio": 550.00, "stock": 35, "cat": "Fuentes de Poder", "img": "https://images.unsplash.com/photo-1587202372616-b43abea06c2a?q=80&w=800"},
            {"nombre": "Gigabyte 750W 80+ Gold Modular", "descripcion": "Fuente de alto rendimiento para equipos top.", "precio": 850.00, "stock": 20, "cat": "Fuentes de Poder", "img": "https://images.unsplash.com/photo-1587202372616-b43abea06c2a?q=80&w=800"},

            # GABINETES
            {"nombre": "Gabinete Delux ATX + Fuente 500W", "descripcion": "Gabinete básico de oficina, incluye fuente genérica.", "precio": 250.00, "stock": 30, "cat": "Gabinetes", "img": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?q=80&w=800"},
            {"nombre": "Gabinete Halion Gamer", "descripcion": "Gabinete con lateral acrílico y 1 ventilador RGB.", "precio": 350.00, "stock": 40, "cat": "Gabinetes", "img": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?q=80&w=800"},
            {"nombre": "NZXT H510 Flow", "descripcion": "Gabinete Mid-Tower premium, panel de cristal templado.", "precio": 700.00, "stock": 20, "cat": "Gabinetes", "img": "https://images.unsplash.com/photo-1587831990711-23ca6441447b?q=80&w=800"},

            # TARJETAS GRÁFICAS
            {"nombre": "NVIDIA GeForce GTX 1650 4GB", "descripcion": "Gráfica de entrada para juegos en 1080p.", "precio": 1200.00, "stock": 20, "cat": "Tarjetas Gráficas", "img": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=800"},
            {"nombre": "AMD Radeon RX 6600 8GB", "descripcion": "Excelente rendimiento 1080p calidad ultra.", "precio": 1800.00, "stock": 25, "cat": "Tarjetas Gráficas", "img": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=800"},
            {"nombre": "NVIDIA GeForce RTX 3060 12GB", "descripcion": "Gráfica muy popular, DLSS y Ray Tracing en 1080p.", "precio": 2400.00, "stock": 30, "cat": "Tarjetas Gráficas", "img": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=800"},
            {"nombre": "NVIDIA GeForce RTX 4060 8GB", "descripcion": "Última generación, DLSS 3.0, bajo consumo.", "precio": 2600.00, "stock": 15, "cat": "Tarjetas Gráficas", "img": "https://images.unsplash.com/photo-1591488320449-011701bb6704?q=80&w=800"},

            # MONITORES
            {"nombre": "Monitor LG 22\" FHD 75Hz", "descripcion": "Monitor básico 1080p, panel IPS.", "precio": 750.00, "stock": 40, "cat": "Monitores", "img": "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?q=80&w=800"},
            {"nombre": "Monitor Samsung 24\" FHD 75Hz", "descripcion": "Bordes delgados, FreeSync, panel IPS.", "precio": 900.00, "stock": 35, "cat": "Monitores", "img": "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?q=80&w=800"},
            {"nombre": "Monitor AOC 24\" 165Hz Gamer", "descripcion": "Ideal para esports, 1ms respuesta, 1080p.", "precio": 1400.00, "stock": 25, "cat": "Monitores", "img": "https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?q=80&w=800"},

            # PERIFÉRICOS
            {"nombre": "Kit Teclado y Mouse Logitech MK120", "descripcion": "Kit básico de oficina alámbrico.", "precio": 120.00, "stock": 60, "cat": "Periféricos", "img": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=800"},
            {"nombre": "Teclado Mecánico Redragon Kumara", "descripcion": "Teclado TKL, switches Outemu Red, RGB.", "precio": 280.00, "stock": 45, "cat": "Periféricos", "img": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?q=80&w=800"},
            {"nombre": "Mouse Gamer Logitech G203", "descripcion": "Sensor preciso de 8000 DPI, RGB LIGHTSYNC.", "precio": 180.00, "stock": 50, "cat": "Periféricos", "img": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?q=80&w=800"}
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

        for _ in range(80):  # Aumentamos a 80 ventas para poblar bien el dashboard
            cliente = random.choice(clientes)
            dias_atras = random.randint(0, 30)
            horas_atras = random.randint(0, 23)
            minutos_atras = random.randint(0, 59)
            fecha_venta = hoy - timedelta(days=dias_atras, hours=horas_atras, minutes=minutos_atras)

            nueva_venta = Venta(user_id=cliente.id, fecha=fecha_venta, total=0.0)
            db.session.add(nueva_venta)
            db.session.flush()

            num_items = random.randint(1, 5)
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
        print("Seeding de Componentes de PC (Precios en Bs) completado.")

if __name__ == "__main__":
    seed_database()