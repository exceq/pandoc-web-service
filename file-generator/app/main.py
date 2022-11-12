import json
from os import getenv

import pypandoc as pd
import requests
from fastapi import FastAPI
from minio.helpers import ObjectWriteResult
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from .queue import QueueConnection
from .storage_connect import *

app_hostname = getenv("APP_HOSTNAME")

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/samples/static"), name="static")

default_css_path: str = 'app/static/resume.css'
default_header_path: str = 'app/samples/templates/header.html'


class Item(BaseModel):
    markdown: str


class GeneratePdfMessage:
    file_id: int
    markdown: str

    def __init__(self, **args):
        self.__dict__ = args


@app.get("/")
async def root():
    return {"message": "Hello World from file-generator"}


def handle_message(ch, method, properties, body: bytes):
    try:
        message: GeneratePdfMessage = json.loads(body, object_hook=lambda d: GeneratePdfMessage(**d))
        html = pd.convert_text(source=message.markdown, format='markdown', to='html',
                               extra_args=['-s', '--section-divs', '-H', default_header_path, '--css',
                                           default_css_path])
        filename = f'{message.file_id}.pdf'
        filepath = f'out/' + filename
        pd.convert_text(source=html, format='html', to='pdf', outputfile=filepath)
        file: ObjectWriteResult = put_file("pdf", filename, filepath)
        os.remove(filepath)
        send_put_request(filename, message)
    except Exception as e:
        print("!!! ERROR !!!", e)


def send_put_request(filename: str, message: GeneratePdfMessage):
    url = f'http://{app_hostname}/resume/{message.file_id}'
    request_body = {"filepath": filename}
    requests_put = requests.put(url, json=request_body, timeout=10)
    requests_put.raise_for_status()


queue: QueueConnection = QueueConnection()
queue.channel.basic_consume(queue=queue.GENERATE_PDF_QUEUE, on_message_callback=handle_message)
queue.channel.start_consuming()
