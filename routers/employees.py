from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from auth.auth import get_current_user, require_admin

from database import get_db
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from services import employee_service
from auth import auth

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/", response_model=list[EmployeeResponse])
def get_employees(
    skip: int = 0,
    limit: int = 5,
    department: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    return employee_service.get_all_employees(
    db,
    skip,
    limit,
    department,
    is_active
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    return employee_service.get_employee(
        db,
        employee_id
    )

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return employee_service.create_employee(
        db,
        employee
    )

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return employee_service.update_employee(
        db,
        employee_id,
        employee
    )


# @router.delete("/{employee_id}")
# def delete_employee(
#     employee_id: int,
#     db: Session = Depends(get_db)
# ):
#     return employee_service.delete_employee(
#         db,
#         employee_id
#     )

@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return employee_service.delete_employee(db, employee_id)


# {
#   "email": "john@test.com",
#   "password": "password123"
# }