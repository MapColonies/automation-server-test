import posixpath
import re
import json
import hashlib
import requests


def url_validator(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def combine_url(base, *args) -> str:
    """
    This method concat / combine and build new url from list parts of url
    :param base : this is the base relative uri
    :param *args : sub directories of the url
    """
    for i in range(len(args)):
        base = posixpath.join(base, args[i])
    return base


def response_parser(resp):
    """
    This method parsing standard request response object to readable data
    :param resp: request response object dict
    :return: status code and content dict
    """
    status_code = resp.status_code
    content_dict = json.loads(resp.text)
    return status_code, content_dict


def load_file_as_bytearray(file_uri):
    """
    This method open file and return bytearray
    :param file_uri: file location
    :return: bytearray
    """
    f = open(file_uri, "rb")
    ba = bytearray(f.read())
    return ba


def generate_unique_fingerprint(bytes_array):
    """
    This method generate using md5 algo, unique fingerprint string for given bytearray
    :param bytes_array: bytes to convert
    :return: fingerprint string
    """
    res = hashlib.md5(bytes_array)
    finger_print_str = res.hexdigest()
    return finger_print_str
