from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

if __name__ == "__main__":

    with app.app_context():

        # crear tablas
        db.create_all()

        # crear admin si no existe
        admin = User.query.filter_by(username="admin").first()

        if not admin:
            admin = User(username="admin", role="admin")
            admin.set_password("1234")

            db.session.add(admin)
            db.session.commit()

            print("Admin creado")

    app.run(debug=True)