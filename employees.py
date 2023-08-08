from config import db
from models import Employee, employees_schema, employee_schema


def read_all():
    employees = Employee.query.all()
    return employees_schema.dump(employees)


def create_employee(employee):
    last_name = employee.get("last_name")
    existing_employee = Employee.query.filter(Employee.last_name == last_name).one_or_none()

    if existing_employee is None:
        new_employee = employee_schema.load(employee, session=db.session)
        db.session.add(new_employee)
        db.session.commit()
        return employee_schema.dump(new_employee), 201
    else:
        abort(
            406,
            f"Employee with last name {last_name} already exists",
        )