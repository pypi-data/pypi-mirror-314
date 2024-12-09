from sys import stdin

from m.utils.console import console
from mm_read.extract import extract_text
from rich.markdown import Markdown
from typer import Typer

from .impl import get_markdown

app = Typer()


@app.command(no_args_is_help=True)
def read(url: str):
    if url == "-":
        content = stdin.read()
        markdown = extract_text(content)
    else:
        markdown = get_markdown(url)

    if console.is_terminal:
        console.print(Markdown(markdown))
    else:
        print(markdown)
