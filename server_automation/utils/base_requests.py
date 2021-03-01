# pylint: disable=line-too-long, invalid-name
"""
This module wrapping http protocol request sending [get, post and etc.]
"""
import logging
import json
import requests
from server_automation.utils import common
_log = logging.getLogger('server.exporter.requests')


def send_post_request(url, body, header=None):
    """ send http post request by providing post full url + body , header is optional, by default:content-type': 'application/json',
    "accept": "*/* """
    common.url_validator(url)
    if not header:
        header = {'content-type': 'application/json', "accept": "*/*"}
    try:
        resp = requests.post(url=url, data=json.dumps(body), headers=header)
        _log.info("response code: %d", resp.status_code)
        _log.info("response message: %s", resp.text)

    except Exception as e:
        _log.error('failed get response with error: %s', str(e))
        raise requests.exceptions.RequestException('failed on getting response data from get response with error message: %s' % str(e))

    return resp


def send_get_request(url):
    """ send http get request by providing get full url """
    common.url_validator(url)
    try:
        resp = requests.get(url)
        _log.debug("response code: %d", resp.status_code)
        _log.debug("response message: %s", resp.content)
        # _log.debug("response message: %s" % resp.text)

    except Exception as e:
        _log.error('failed get response with error: %s', str(e))
        raise requests.exceptions.RequestException("failed on getting response data from get response with error message: %s" % str(e))

    return resp
