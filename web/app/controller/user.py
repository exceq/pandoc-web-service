from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from core.db.models import User, File
from deps import get_db
from model.resume import FileDto
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


@router.get("/info")
async def info(user_id: int, db: Session = Depends(get_db)):
    user: User = db.query(User).filter_by(id=user_id).one()
    files: List[File] = db.query(File).filter_by(user_id=user_id).all()
    files_dto = [FileDto(created=file.created, id=file.id, filename=file.path_to_pdf) for file in files]
    return {"user": user, "files": files_dto}


def find_by_username(username: str, db: Session):
    return db.query(User).filter_by(username=username).one_or_none()
