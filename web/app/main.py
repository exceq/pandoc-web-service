from fastapi import FastAPI
import pypandoc as pd
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class ConvertRequest(BaseModel):
    markdown_text: str
    format: str
    to: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/convert", response_class=HTMLResponse)
async def say_hello(request: ConvertRequest):
    return pd.convert_text(source=request.markdown_text, format=request.format, to=request.to)
