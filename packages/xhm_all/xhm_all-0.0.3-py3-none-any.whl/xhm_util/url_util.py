import urllib.parse


def encode(url):
    """urlencode之后，不会再二次encode，防止链接打不开"""
    # Check if the URL contains any non-ASCII characters
    if any(ord(c) >= 128 for c in url):
        # If it does, encode the URL using urllib.parse.quote
        encoded_url = urllib.parse.quote(url, safe='/:?&=', encoding='utf-8')
        return encoded_url
    else:
        # If it doesn't, return the original URL
        return url
