import hashlib
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


def hashed_password(password, salt):
    return hashlib.md5((password + salt).encode()).hexdigest()


def add_query_param(url, key, value):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params[key] = value
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query_string))
    return new_url
