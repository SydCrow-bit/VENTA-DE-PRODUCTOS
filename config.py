import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno de Python
load_dotenv()
# --------------------------------------
api_key = os.environ.get("GEMINI_API_KEY")
print("=========================================")
print(f"DEBUG - GEMINI_API_KEY leída: '{api_key}'")
print("=========================================")
# --------------------------------------
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        "mysql+pymysql://root@localhost:3306/db_venta_electronicos"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GEMINI_API_KEY = api_key