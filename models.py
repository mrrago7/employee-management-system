from app import db

class Employee(db.Model):
    __tablename__="employees"

    id=db.Column(db.Integer, primary_key=True)
    full_name=db.Column(db.String(100), nullable=False)
    position=db.Column(db.String(100), nullable=False)
    hire_date=db.Column(db.Date, nullable=False)
    salary=db.Column(db.Numeric(precision=10, scale=2))
    manager_id=db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True)

    manager=db.relationship("Employee", remote_side="Employee.id", back_populates="subordinates")
    subordinates=db.relationship("Employee", back_populates="manager")


