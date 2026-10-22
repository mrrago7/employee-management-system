from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Employee

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
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


    page = request.args.get("page", 1, type=int)

    pagination = db.paginate(
        query,
        page=page,
        per_page=500,
        error_out=False
    )

    employees = pagination.items

    return render_template(
        "employees.html",
        employees=employees,
        search=search,
        sort_fields=sort_fields,
        order=order,
        pagination=pagination
    )

@app.route("/employees/<int:employee_id>/manager", methods=['POST'])
def change_manager(employee_id):
    position=["CEO", "Manager", "Team Lead", "Senior Developer", "Developer"]
    
    employee=db.session.get(Employee, employee_id)
    manager_id = request.form.get("manager_id", type=int)

    if employee:
        manager = db.session.get(Employee, manager_id) if manager_id else None
        
        if manager:
            if manager.id!=employee.id:
                if employee.position!="CEO":
                    for i in range(5):
                        if employee.position==position[i]:
                            k=i
                            break
                    else:
                        flash("No such position")
                        return redirect("/employees")


                    if manager.position==position[k-1]:
                        employee.manager_id=manager.id
                        db.session.commit()
                        flash("Success, the leader has been changed!")
                        return redirect("/employees")

                    else:
                        flash("The manager is not suitable")
                        return redirect("/employees")

                else:
                    flash("CEO doesn't have manager")
                    return redirect("/employees")
                
            else:
                        flash("Employee can't be their own manager")
                        return redirect("/employees")

        else:
            flash("Manager not found")
            return redirect("/employees")

    else:
        flash("Employee not found")
        return redirect("/employees")



@app.route("/api/managers", methods=["GET"])
def search_managers():
    search = request.args.get("search", "").strip()
    employee_id = request.args.get("employee_id", type=int)

    if len(search) < 3 or not employee_id:
        return {"managers": []}

    employee = db.session.get(Employee, employee_id)

    if not employee or employee.position == "CEO":
        return {"managers": []}

    positions = ["CEO","Manager","Team Lead","Senior Developer","Developer"]

    if employee.position not in positions:
        return {"managers": []}

    level = positions.index(employee.position)

    query = db.select(Employee).where(
        Employee.position == positions[level - 1],
        Employee.full_name.ilike(f"%{search}%"),
        Employee.id != employee.id
    ).limit(10)

    managers = db.session.execute(query).scalars().all()

    return {
        "managers": [
            {
                "id": manager.id,
                "full_name": manager.full_name,
                "position": manager.position
            }
            for manager in managers
        ]
    }