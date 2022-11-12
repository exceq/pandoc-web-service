import pypandoc as pd

from model.resume import Item
from service import cache
from service.hash_util import generate_hash

CACHE_PREVIEW_TIME = 10 * 60  # 10 минут


def get_preview(item: Item):
    hash_value: str = generate_hash(item.markdown)
    return cache.get_or_load(hash_value, CACHE_PREVIEW_TIME, lambda: get_html_from_md(item))


def get_html_from_md(item: Item):
    print("converting...")
    return pd.convert_text(source=item.markdown, format='markdown', to='html',
                           extra_args=['-s', '--section-divs'])
