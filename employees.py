from models import Employee, employees_schema, employee_schema


def read_all():
    print('read_all fires')
    employees = Employee.query.all()
    print(employees)
    return employees_schema.dump(employees)


