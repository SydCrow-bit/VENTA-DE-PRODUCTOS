class Config:
    SECRET_KEY = "supersecretkey"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/db_venta_electronicos"

    SQLALCHEMY_TRACK_MODIFICATIONS = False