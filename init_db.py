from app import app, db
from models import Employee

with app.app_context():
    db.create_all()