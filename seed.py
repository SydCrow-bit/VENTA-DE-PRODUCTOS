from app import create_app
from app.extensions import db
from app.models import Categoria, Producto

app = create_app()

def run_seeder():
    with app.app_context():
        if Categoria.query.first() or Producto.query.first():
            respuesta = input("La base de datos ya contiene registros. ¿Deseas limpiar los datos y poblar nuevamente? (s/n): ")
            
            if respuesta.lower() in ['s', 'si', 'y', 'yes']:
                Producto.query.delete()
                Categoria.query.delete()
                db.session.commit()
                print("Datos anteriores eliminados correctamente.")
            else:
                print("Operacion cancelada.")
                return

        cat_laptops = Categoria(
            nombre="Laptops", 
            descripcion="Computadoras portátiles de alto rendimiento"
        )
        cat_smartphones = Categoria(
            nombre="Smartphones", 
            descripcion="Teléfonos móviles de última generación"
        )
        cat_accesorios = Categoria(
            nombre="Accesorios", 
            descripcion="Cables, cargadores y periféricos"
        )

        db.session.add_all([cat_laptops, cat_smartphones, cat_accesorios])
        db.session.commit()

        prod_1 = Producto(
            nombre="Laptop Gamer Xtreme",
            descripcion="Procesador de última generación, 16GB RAM",
            precio=12500.50,
            stock=15,
            categoria_id=cat_laptops.id
        )
        prod_2 = Producto(
            nombre="Ultrabook Ejecutiva",
            descripcion="Diseño ultraligero, batería de 15 horas",
            precio=8900.00,
            stock=8,
            categoria_id=cat_laptops.id
        )
        prod_3 = Producto(
            nombre="Smartphone Galaxy Pro",
            descripcion="Cámara de 108MP, 256GB almacenamiento",
            precio=6500.00,
            stock=30,
            categoria_id=cat_smartphones.id
        )
        prod_4 = Producto(
            nombre="Auriculares Inalámbricos SoundMax",
            descripcion="Cancelación de ruido activa",
            precio=1200.00,
            stock=50,
            categoria_id=cat_accesorios.id
        )

        db.session.add_all([prod_1, prod_2, prod_3, prod_4])
        db.session.commit()

        print("Base de datos poblada exitosamente con categorias y productos.")

if __name__ == "__main__":
    run_seeder()