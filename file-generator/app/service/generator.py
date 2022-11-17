import json
from os import getenv

import pypandoc as pd
import requests
from minio.helpers import ObjectWriteResult
from pydantic import BaseModel
from uvicorn.main import logger

from service.storage_connect import *

app_hostname = getenv("APP_HOSTNAME")
default_css_path: str = 'samples/static/resume.css'
default_css_frame_path: str = 'samples/static/frame.css'
default_header_path: str = 'samples/templates/header.html'

html_to_pdf_args = ['-s',
                    '--section-divs',
                    '-H', default_header_path,
                    '--css', default_css_path,
                    '--css', default_css_frame_path,
                    '--pdf-engine=wkhtmltopdf',
                    '--pdf-engine-opt=--enable-local-file-access',
                    '-V', 'margin-top=0',
                    '-V', 'margin-left=0',
                    '-V', 'margin-right=0',
                    '-V', 'margin-bottom=0',
                    '-V', 'title:""',
                    '--to=html' # иначе по умолчанию генерирует в latex, а это не подходит для wkhtmltopdf
                    ]
md_to_html_args = ['-s',
                   '--section-divs',
                   '-H', default_header_path,
                   '--css', default_css_path]

class Item(BaseModel):
    markdown: str


class GeneratePdfMessage:
    file_id: int
    markdown: str

    def __init__(self, **args):
        self.__dict__ = args


def handle_message(body: bytes):
    message: GeneratePdfMessage = json.loads(body, object_hook=lambda d: GeneratePdfMessage(**d))
    html = pd.convert_text(source=message.markdown, format='markdown', to='html', extra_args=md_to_html_args)
    filename = f'{message.file_id}.pdf'
    filepath = f'out/' + filename
    if not os.path.exists('out'):
        os.mkdir('out')
    pd.convert_text(source=html, format='html', to='pdf', outputfile=filepath, extra_args=html_to_pdf_args)
    file: ObjectWriteResult = put_file("pdf", filename, filepath)
    # todo save pandoc output file in memory
    os.remove(filepath)
    send_put_request(filename, message)
    logger.info(f'success file_id={message.file_id}, filename={filename}')


def send_put_request(filename: str, message: GeneratePdfMessage):
    url = f'http://{app_hostname}/resume/{message.file_id}'
    request_body = {"filepath": filename}
    requests_put = requests.put(url, json=request_body, timeout=10)
    requests_put.raise_for_status()
