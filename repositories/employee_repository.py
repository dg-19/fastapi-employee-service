from sqlalchemy.orm import Session
from models import Employee
from sqlalchemy.exc import IntegrityError


def get_all_employees(
    db: Session,
    skip: int,
    limit: int,
    department: str | None,
    is_active: bool | None
):
    query = db.query(Employee)

    if department:
        query = query.filter(
            Employee.department == department
        )

    if is_active is not None:
        query = query.filter(
            Employee.is_active == is_active
        )

    query = query.offset(skip).limit(limit)

    return query.all()


def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def get_employee_by_email(db: Session, email: str):
    return (
        db.query(Employee)
        .filter(Employee.email == email)
        .first()
    )

def create_employee(
    db: Session,
    name: str,
    email: str,
    age: int,
    salary: int,
    department: str
):
    db_employee = Employee(
        name=name,
        email=email,
        age=age,
        salary=salary,
        department=department
    )

    db.add(db_employee)
    
    try:
        db.commit()
        db.refresh(db_employee)
    except IntegrityError:
        db.rollback()
        raise

    return db_employee


def update_employee(
    db: Session,
    employee_id: int,
    name: str,
    email: str,
    age: int,
    salary: int,
    department: str
):
    db_employee = get_employee_by_id(db, employee_id)

    if not db_employee:
        return None

    db_employee.name = name
    db_employee.email = email
    db_employee.age = age
    db_employee.salary = salary
    db_employee.department = department

    try:
        db.commit()
        db.refresh(db_employee)
    except Exception:
        db.rollback()
        raise

    return db_employee


def delete_employee(db: Session, employee: Employee):
    try:
        db.delete(employee)
        db.commit()
    except Exception:
        db.rollback()
        raise