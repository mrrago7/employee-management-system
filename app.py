from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Employee

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql+psycopg://postgres:2952246@localhost:5432/employee_db")
db.init_app(app)


@app.route("/employees", methods=['GET'])
def get_employees():    
    search = request.args.get("search", "")
    query=db.select(Employee)

    search_splitted=search.split(" ")

    if len(search_splitted)==1:
        query=query.where(Employee.full_name.ilike(f"%{search}%"))

    elif len(search_splitted)==2:
        query = query.where(db.and_(
        Employee.full_name.ilike(f"%{search_splitted[0]}%"),
        Employee.full_name.ilike(f"%{search_splitted[1]}%")))


    order=request.args.get("order", "asc")
    sort_fields = request.args.getlist("sort")
    allowed_fields = {"salary": Employee.salary,"hire_date": Employee.hire_date}

    for field in sort_fields:
        if field in allowed_fields:
            column = allowed_fields[field]

            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())


    employees=db.session.execute(query).scalars().all()

    return render_template("employees.html",employees=employees,search=search,sort_fields=sort_fields,order=order)

