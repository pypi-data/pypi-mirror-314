def extract_text(html: str, baseurl=""):
    from readability import parse

    article = parse(html, keep_classes=True)

    from .parse import to_markdown

    if article.content:
        body = to_markdown(article.content, baseurl)
    elif article.text_content:
        body = article.text_content
    else:
        body = to_markdown(html, baseurl)

    return f"# {article.title}\n\n{body}" if article.title else body
