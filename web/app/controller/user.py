from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from core.db.models import User
from deps import get_db
from model.user import UserDto, RegisterRequest

router = APIRouter()


@router.post("/register", response_model=UserDto)
async def register(req: RegisterRequest, db: Session = Depends(get_db)):
    found_user: User = find_by_username(req.username, db)
    if found_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"username '{req.username}' уже занят")
    user = User(username=req.username)
    db.add(user)
    db.commit()
    return user


def find_by_username(username: str, db: Session):
    return db.query(User).filter_by(username=username).one_or_none()
