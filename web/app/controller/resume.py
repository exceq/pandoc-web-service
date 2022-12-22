import urllib3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse, Response
from uvicorn.main import logger

from core.db.models import File, User
from deps import get_db
from model.queue import GeneratePdfMessage
from model.resume import Item, SavePdfRequest, UpdateFilePathRequest
from service.hash_util import generate_hash
from service.queue import QueueConnection
from service.resume import get_preview, get_preview_by_id
from service.storage import client

router = APIRouter()

queue = QueueConnection()


@router.get("/example", response_class=HTMLResponse)
async def example():
    return open('samples/content/resume.md', 'r').read()


@router.post("/preview", response_class=HTMLResponse)
async def preview(item: Item):
    return get_preview(item)


@router.get("/{id}", response_class=HTMLResponse)
async def preview_by_id(id: int, db: Session = Depends(get_db)):
    return get_preview_by_id(id, db)


@router.delete("/{id}")
async def delete_resume(id: int, db: Session = Depends(get_db)):
    db.query(File).filter_by(id=id).delete()
    db.commit()
    # todo delete file in minio
    return {'message': 'ok'}


class OctetStreamResponse(Response):
    media_type = "application/octet-stream"


class PdfResponse(Response):
    media_type = "application/pdf"


@router.get("/download/{id}")
async def download(id: int, db: Session = Depends(get_db)):
    file: File = db.query(File).filter_by(id=id).one_or_none()
    if not file:
        return Response({"message", "File not found"}, status_code=404)

    obj = None
    try:
        obj: urllib3.response.HTTPResponse = client.get_object('pdf', file.path_to_pdf)
        return Response(obj.data, media_type='application/pdf')
    except Exception as e:
        logger.error(e)
    finally:
        if obj:
            obj.close()
            obj.release_conn()


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

    hex_dig = generate_hash(text)
    file: File = try_find_saved_pdf(req, hex_dig, db)
    logger.info(file)
    if file:
        return await download(file.id, db=db) if file.path_to_pdf else 'wait'
    file = File(user_id=req.user_id, full_text=text, hash=hex_dig)
    db.add(file)
    db.commit()
    try:
        queue.send_generate_pdf_message(GeneratePdfMessage(file.id, file.full_text))
    # except ConnectionResetError as e:
    except Exception as e:
        db.delete(file)
        db.commit()
        return "error"
    return "ok"


def try_find_saved_pdf(req: SavePdfRequest, hex_dig: str, db: Session) -> File:
    return db.query(File).filter_by(user_id=req.user_id, hash=hex_dig).one_or_none()
