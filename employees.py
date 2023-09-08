import os
import requests
from flask import abort, jsonify, request

from config import db
from models import Employee, EmployeeSchema, employees_schema, employee_schema


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": f"MCQ <mailgun@{domain}>",
            "to": [to],
            "subject": [subject],
            "text": [body],
        },
    )


def read_all():
    employees = Employee.query.all()
    return employees_schema.dump(employees)


def create_employee(employee):
    email = employee.get("email")
    existing_employee = Employee.query.filter(Employee.email == email).one_or_none()

    if existing_employee is None:
        new_employee = employee_schema.load(employee, session=db.session)
        db.session.add(new_employee)
        db.session.commit()

        first_name = employee.get("first_name")
        last_name = employee.get("last_name")

        send_simple_message(
            to=os.getenv("ADMIN_EMAIL"),
            subject=f"An employee was successfully added to the HR REST API.",
            body=f"Employee added: {first_name} {last_name}",
        )

        return employee_schema.dump(new_employee), 201
    else:
        abort(
            406,
            f"Employee with same email already exists",
        )


def search_employees():
    search_term = ""
    try:
        query_params = request.args
        query = Employee.query

        if "first_name" in query_params:
            search_term = query_params["first_name"]
            query = query.filter(db.or_(Employee.first_name.ilike(search_term)))

        if "like_first_name" in query_params:
            search_term = query_params["like_first_name"]
            query = query.filter(
                db.or_(Employee.first_name.ilike("%" + search_term + "%"))
            )

        if "last_name" in query_params:
            search_term = query_params["last_name"]
            query = query.filter(db.or_(Employee.last_name.ilike(search_term)))

        if "like_last_name" in query_params:
            search_term = query_params["like_last_name"]
            query = query.filter(
                db.or_(Employee.last_name.ilike("%" + search_term + "%"))
            )

        if "gender" in query_params:
            search_term = query_params["gender"]
            query = query.filter(db.or_(Employee.gender.ilike(search_term)))

        if "base_salary_eq" in query_params:
            search_term = query_params["base_salary_eq"]
            query = query.filter(db.or_(Employee.base_salary == search_term))

        if "base_salary_gte" in query_params:
            search_term = query_params["base_salary_gte"]
            query = query.filter(db.or_(Employee.base_salary >= search_term))

        if "base_salary_lte" in query_params:
            search_term = query_params["base_salary_lte"]
            query = query.filter(db.or_(Employee.base_salary <= search_term))

        employees = query.all()
        result = []

        if len(employees) > 0:
            for employee in employees:
                result.append(
                    {
                        "id": employee.id,
                        "first_name": employee.first_name,
                        "last_name": employee.last_name,
                        "gender": employee.gender,
                        "email": employee.email,
                        "base_salary": employee.base_salary,
                    }
                )
            return jsonify(result)
    except Exception as e:
        print(
            f"there was an error searching for employee data using the search term: {search_term}: {e}"
        )


def update_employee(employee):
    employee_id = employee.get("id")
    try:
        existing_employee = Employee.query.filter(
            Employee.id == employee_id
        ).one_or_none()

        if existing_employee is None:
            abort(
                406,
                f"Employee record does not exist so it cannot be updated",
            )
        else:
            updated_employee = employee_schema.load(employee, session=db.session)
            updated_employee.id = existing_employee.id
            db.session.add(updated_employee)
            db.session.commit()
            return employee_schema.dump(updated_employee), 200
    except Exception as e:
        print(
            f"there was an error updating employee data for employee: {employee_id}: {e}"
        )


def patch_employee(employee):
    employee_id = employee.get("id")
    existing_employee = Employee.query.filter(Employee.id == employee_id).one_or_none()

    if existing_employee is None:
        abort(
            406,
            f"Employee record does not exist so it cannot be updated",
        )
    else:
        updated_employee = employee_schema.load(employee, session=db.session)
        updated_employee.id = existing_employee.id
        db.session.add(updated_employee)
        db.session.commit()
        return employee_schema.dump(updated_employee), 200
