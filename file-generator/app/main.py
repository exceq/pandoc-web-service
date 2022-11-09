import time

import pypandoc as pd
from fastapi import FastAPI
from minio.helpers import ObjectWriteResult
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from .storage_connect import *


class Item(BaseModel):
    markdown: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/samples/static"), name="static")

default_css_path: str = 'app/static/resume.css'
default_header_path: str = 'app/samples/templates/header.html'


@app.get("/")
async def root():
    return {"message": "Hello World from file-generator"}


@app.post("/pdf-to-minio")
async def generate_pdf1(item: Item):
    html = pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs', '-H', default_header_path, '--css', default_css_path])
    filename = f'pdf-{time.time()}.pdf'
    filepath = f'./out/' + filename
    pd.convert_text(source=html, format='html', to='pdf', outputfile=filepath)
    # todo put request with bucket_name, filename
    file: ObjectWriteResult = put_file("pdf", filename, filepath)
    os.remove(filepath)
    return {"bucket": file.bucket_name, "filename": file.object_name}
