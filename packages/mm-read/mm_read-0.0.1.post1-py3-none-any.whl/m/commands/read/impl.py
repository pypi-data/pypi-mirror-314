from pathlib import Path

from mm_read.extract import extract_text
from mm_read.fetch import request


def get_markdown(url: str):
    if url.startswith("http"):
        html, baseurl = request(url)
    else:
        html = Path(url).read_text()
        baseurl = url

    return extract_text(html, baseurl)
