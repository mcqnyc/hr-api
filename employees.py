from flask import abort, jsonify, request

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


def search_employees(search_term=None):
    # try:
    #     if search_term is None:
    #         employee = Employee.query.filter().all()
    #         employee_schema = EmployeeSchema(many=True)
    #         return employee_schema.jsonify(employee)
    #     elif search_term ==

    query_params = request.args
    print(f'params = {query_params}')
    print(f'request url = {request.url}')
    
    query = Employee.query
    if 'last_name' in query_params:
        last_name = query_params['last_name']
        
        query = query.filter(db.or_(
            # Employee.first_name.ilike(name),
            Employee.last_name.ilike(last_name)
        ))
        print(f'query: {query}')
    # Add other search options like create date, modified date, gender, pay range.
        employees = query.all()
        print(f'employees: {employees}')
        result = []
        
        if len(employees) > 0:
            for employee in employees:
                print(f'employee: {employee}')
                result.append({
                    'id': employee.id,
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'gender': employee.gender,
                    'email': employee.email,
                    'base_salary': employee.base_salary
                })
            # return employee_schema.jsonify(result)
            return jsonify(result)
        else:
            abort(
                404,
                # f"Employee with name {first_name} does not exist",
                # f"Employee cannot be found",
                f"Employee {last_name} cannot be found",
            )
        