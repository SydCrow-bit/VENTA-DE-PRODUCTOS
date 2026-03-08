from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

if __name__ == "__main__":
    # If you aren't running db.create_all(), you don't need the context block here
    app.run(debug=True)