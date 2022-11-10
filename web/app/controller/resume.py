import hashlib
import logging

import pypandoc as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse

from core.db.models import File, User
from deps import get_db
from model.queue import GeneratePdfMessage
from model.resume import Item, SavePdfRequest, UpdateFilePathRequest
from service.queue import QueueConnection

router = APIRouter()

queue = QueueConnection()

@router.get("/example", response_class=HTMLResponse)
async def example():
    return open('samples/content/resume.md', 'r').read()


@router.post("/preview", response_class=HTMLResponse)
async def say_hello(item: Item):
    return pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs'])


@router.put("/{file_id}")
async def update_resume(file_id: int, req: UpdateFilePathRequest, db: Session = Depends(get_db)):
    file: File = db.query(File).filter_by(id=file_id).one()
    file.path_to_pdf = req.filepath
    db.commit()
    return "ok"


@router.post("/save-pdf")
async def save_pdf(req: SavePdfRequest, db: Session = Depends(get_db)):
    text = req.markdown.strip()
    if not req.user_id or not text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Необходимо указать user_id")
    user = db.query(User).filter_by(id=req.user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с id '{req.user_id}' не найден")

    hex_dig = hashlib.sha256(bytes(text, 'utf-8')).hexdigest()
    file = File(user_id=req.user_id, full_text=text, hash=hex_dig)
    db.add(file)
    db.commit()
    queue.send_generate_pdf_message(GeneratePdfMessage(file.id, file.full_text))
    return "ok"
