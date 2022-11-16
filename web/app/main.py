from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from controller.resume import router as resume_router
from controller.user import router as user_router
from core.db.models import Base
from core.db.session import engine

# Base.metadata.create_all(engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="samples/static"), name="static")

app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(resume_router, prefix='/resume', tags=['Resume'])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, e: Exception):
    print(e)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {
                "message": e.message if hasattr(e, 'message') else "Ошибка!",
                "type": str(e)
            }
        ),
    )
