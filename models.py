from datetime import datetime
from marshmallow_sqlalchemy import fields

from config import db, ma


class Note(db.Model):
    __tablename__ = "Note"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True


class Employee(db.Model):
    __tablename__ = "Employee"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    gender = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    base_salary = db.Column(db.Integer)
    created = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated = db.Column(
        db.DateTime, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        Note,
        backref="employee",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    notes = fields.Nested(NoteSchema, many=True)


note_schema = NoteSchema()
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
