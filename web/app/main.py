import pypandoc as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/samples/static"), name="static")


class Item(BaseModel):
    markdown: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/example", response_class=HTMLResponse)
async def example():
    return open('app/samples/content/resume.md', 'r').read()


@app.post("/preview", response_class=HTMLResponse)
async def say_hello(item: Item):
    return pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs'])
