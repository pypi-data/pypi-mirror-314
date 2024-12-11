import urllib.parse


def urlencode(text: str) -> str:
    return urllib.parse.quote(text, safe="")
