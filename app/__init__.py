# IMPORTS NATIVOS DEL SISTEMA.
import os
import bcrypt

# IMPORTS NATIVOS DEL FRAMEWORK.
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI"
)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")


jwt = JWTManager(app)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
ma = Marshmallow(app)

load_dotenv()

from app.views import views
