from datetime import datetime
from config import app, db
from models import Employee, Note

EMPLOYEE_NOTES = [
    {
        "last_name": "Fairy",
        "first_name": "Tooth",
        "gender": "F",
        "email": "teeth@gmail.com",
        "base_salary": 100000,
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "last_name": "Ruprecht",
        "first_name": "Knecht",
        "gender": "M",
        "email": "Ruprecht@gmail.com",
        "base_salary": 70000,
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "last_name": "Bunny",
        "first_name": "Easter",
        "gender": "M",
        "email": "bunny@aol.com",
        "base_salary": 80000,
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in EMPLOYEE_NOTES:
        new_employee = Employee(
            last_name=data.get("last_name"),
            first_name=data.get("first_name"),
            gender=data.get("gender"),
            email=data.get("email"),
            base_salary=data.get("base_salary"),
        )
        for content, timestamp in data.get("notes", []):
            new_employee.notes.append(
                Note(
                    content=content,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(new_employee)
    db.session.commit()
