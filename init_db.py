from app import app
from extensions import db
from models import Employee

with app.app_context():
    db.create_all()