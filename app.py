from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Employee

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql+psycopg://postgres:2952246@localhost:5432/employee_db")
db.init_app(app)


@app.route("/employees", methods=['GET'])
def get_employees():
    employees=db.session.execute(db.select(Employee)).scalars().all()

    return render_template("employees.html", employees=employees)
