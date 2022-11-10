from fastapi import FastAPI
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
