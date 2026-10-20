from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql+psycopg://postgres:2952246@localhost:5432/employee_db")

db = SQLAlchemy(app)