import pypandoc as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel


class Item(BaseModel):
    markdown: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/samples/static"), name="static")

default_css_path: str = '/static/resume.css'
default_header_path: str = 'app/samples/templates/header.html'


@app.get("/")
async def root():
    return {"message": "Hello World from file-generator"}


@app.get("/example", response_class=HTMLResponse)
async def example():
    return open('app/samples/content/resume.md', 'r').read()


@app.get("/preview", response_class=HTMLResponse)
async def say_hello(markdown: str):
    return make_good(markdown)


@app.post("/preview", response_class=HTMLResponse)
async def say_hello(item: Item):
    return pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs'])


@app.get("/resume", response_class=HTMLResponse)
async def say_hello1():
    return make_good(open('app/samples/content/resume.md').read())


def make_good(markdown):
    return pd.convert_text(source=markdown, format='markdown', to='html',
                           extra_args=['-c', default_css_path, '-H', default_header_path, '-s', '--section-divs'])
