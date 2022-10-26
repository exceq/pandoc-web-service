import time

import pypandoc as pd
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse


class Item(BaseModel):
    markdown: str


app = FastAPI()

default_css_path: str = 'app/static/resume.css'
default_header_path: str = 'app/samples/templates/header.html'


@app.get("/")
async def root():
    return {"message": "Hello World from file-generator"}


@app.post("/pdf", response_class=FileResponse)
async def generate_pdf(item: Item):
    html = pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs', '-H', default_header_path, '--css', default_css_path])
    filename = f'/app/out/pdf-{time.time()}.pdf'
    text = pd.convert_text(source=html, format='html', to='pdf', outputfile=filename)
    return FileResponse(filename, media_type='application/octet-stream', filename='file.pdf')
