from mimesis import Person, Generic
import random
from models import Employee
from app import app, db

ceo_salary=[250000, 400000]
manager_salary=[100000, 160000]
team_lead_salary=[80000, 130000]
senior_developer_salary=[70000, 115000]
developer_salary=[45000, 85000]

staff=[]

managers=[]
team_leads=[]
senior_developers=[]

person=Person("en")
generic=Generic("en")

for i in range(1):
    ceo=Employee()
    ceo.full_name=person.full_name()
    ceo.hire_date=generic.datetime.date()
    ceo.manager_id=None
    ceo.position='CEO'
    ceo.salary=round(random.randint(*ceo_salary), -2)
    staff.append(ceo)

for i in range(10):
    manager=Employee()
    manager.full_name=person.full_name()
    manager.hire_date=generic.datetime.date()
    manager.manager=ceo
    manager.position='Manager'
    manager.salary=round(random.randint(*manager_salary), -2)
    managers.append(manager)
    staff.append(manager)

for i in range(100):
    team_lead=Employee()
    team_lead.full_name=person.full_name()
    team_lead.hire_date=generic.datetime.date()
    team_lead.manager=random.choice(managers)
    team_lead.position='Team Lead'
    team_lead.salary=round(random.randint(*team_lead_salary), -2)
    team_leads.append(team_lead)
    staff.append(team_lead)        

for i in range(1000):
    senior_developer=Employee()
    senior_developer.full_name=person.full_name()
    senior_developer.hire_date=generic.datetime.date()
    senior_developer.manager=random.choice(team_leads)
    senior_developer.position='Senior Developer'
    senior_developer.salary=round(random.randint(*senior_developer_salary), -2)
    senior_developers.append(senior_developer)
    staff.append(senior_developer)  

for i in range(48889):
    developer=Employee()
    developer.full_name=person.full_name()
    developer.hire_date=generic.datetime.date()
    developer.manager=random.choice(senior_developers)
    developer.position='Developer'
    developer.salary=round(random.randint(*developer_salary), -2)
    staff.append(developer)  


with app.app_context():
    db.session.add_all(staff)
    db.session.commit()
