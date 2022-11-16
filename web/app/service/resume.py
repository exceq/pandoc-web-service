from typing import List

import pypandoc as pd
from sqlalchemy.orm import Session

from core.db.models import File
from model.resume import Item
from service import cache
from service.hash_util import generate_hash

CACHE_PREVIEW_TIME = 10 * 60  # 10 минут
default_header_path: str = 'templates/header.html'


def get_preview_by_id(id: int, db: Session):
    file: File = db.query(File).filter_by(id=id).one()
    return get_preview(item=Item(markdown=file.full_text))


def get_preview(item: Item, with_css: bool = False, with_header_template: bool = False):
    hash_value: str = f'hash-{generate_hash(item.markdown)}-css-{str(with_css)}-header-{str(with_header_template)}'
    return cache.get_or_load(hash_value,
                             CACHE_PREVIEW_TIME,
                             lambda: get_html_from_md(item, with_css, with_header_template))


def get_html_from_md(item: Item, with_css: bool = False, with_header_template: bool = False):
    print("converting...")
    args: List = ['-s', '--section-divs']
    if with_css:
        args += ['--css', '/static/resume.css']
    if with_header_template:
        args += ['-H', default_header_path]
    return pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=args)
