def log(*messages):
    try:
        from m.utils.console import console

        console.print(*messages)

    except ModuleNotFoundError:
        print(*messages)


def request(url: str):
    from niquests import get

    res = get(url)

    if not res.ok:
        log(res.status_code, res.reason)

    assert res.text is not None, res

    return res.text, res.url or url
