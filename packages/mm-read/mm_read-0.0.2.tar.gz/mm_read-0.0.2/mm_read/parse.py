import re

sub_trailing_spaces = re.compile(r"[ \t]+$", re.MULTILINE)
sub_multiple_lines = re.compile(r"\n{3,}")


def post_process(text: str):
    text = text.replace("\r", "")
    text = sub_trailing_spaces.sub("", text)
    text = sub_multiple_lines.sub("\n\n", text)
    return text


def to_markdown(html: str, baseurl: str):
    from html2text import html2text

    md = html2text(html, baseurl, bodywidth=0)

    return post_process(md)
