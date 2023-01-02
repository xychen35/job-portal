from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.repository.users import create_new_user

router = APIRouter()

@router.post("/create-user", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session=Depends(get_db)):
    user = create_new_user(user, db)
    return user