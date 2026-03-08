from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Ya no usamos db.create_all(), las migraciones se encargan de eso
    app.run(debug=True)