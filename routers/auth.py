from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import LoginRequest, TokenResponse
from services import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return auth_service.login(db, login_data)