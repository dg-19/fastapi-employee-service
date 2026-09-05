from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from repositories import employee_repository
from schemas import EmployeeCreate, EmployeeUpdate


def get_all_employees(
    db: Session,
    skip: int,
    limit: int,
    department: str,
    is_active: bool
):
    return employee_repository.get_all_employees(
    db,
    skip,
    limit,
    department,
    is_active
    )


def get_employee(db: Session, employee_id: int):
    employee = employee_repository.get_employee_by_id(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


def create_employee(
    db: Session,
    employee: EmployeeCreate
):
    # Business rules can go here.
    existing_employee = employee_repository.get_employee_by_email(
        db,
        employee.email
    )

    if existing_employee:
        raise HTTPException(
            status_code=409,
            detail="Employee already exists"
        )

    try:
        return employee_repository.create_employee(
            db,
            employee.name,
            employee.email,
            employee.age,
            employee.salary,
            employee.department
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    existing_employee = employee_repository.get_employee_by_id(
        db,
        employee_id
    )

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_email_employee = employee_repository.get_employee_by_email(
        db,
        employee.email
    )

    if (
        existing_email_employee
        and existing_email_employee.id != employee_id
    ):
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return employee_repository.update_employee(
        db,
        employee_id,
        employee.name,
        employee.email,
        employee.age,
        employee.salary,
        employee.department
    )


def delete_employee(db: Session, employee_id: int):

    employee = employee_repository.get_employee_by_id(
        db,
        employee_id
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee_repository.delete_employee(
        db,
        employee
    )

    return {"message": "Employee deleted successfully"}