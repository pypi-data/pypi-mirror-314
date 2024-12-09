from sys import stdout

from m.utils.console import console
from rich.markdown import Markdown
from typer import Typer

from .impl import get_markdown

app = Typer()


@app.command(no_args_is_help=True)
def read(url: str):
    if stdout.isatty():
        console.is_dumb_terminal
        console.print(Markdown(get_markdown(url)))
    else:
        print(get_markdown(url))
