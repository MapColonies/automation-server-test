import requests
import json
import logging
from server_automation.utils import common
_log = logging.getLogger('server.exporter.requests')


def send_post_request(url, body, header=None):
    common.url_validator(url)
    if not header:
        header = {'content-type': 'application/json', "accept": "*/*"}
        try:
            resp = requests.post(url=url, data=json.dumps(body), headers=header)
            _log.info("response code: %d" % resp.status_code)
            _log.info("response message: %s" % resp.text)
            return resp
        except Exception as e:
            _log.error('failed get response with error: %s' % (str(e)))
            raise Exception("failed on getting response data from get response with error message: %s" % (str(e)))


def send_get_request(url, header=None):
    common.url_validator(url)
    if not header:
        # header = {'content-type': 'application/json', "accept": "*/*"}
        try:
            resp = requests.get(url)
            _log.debug("response code: %d" % resp.status_code)
            _log.debug("response message: %s" % resp.content)
            # _log.debug("response message: %s" % resp.text)
            return resp

        except Exception as e:
            _log.error('failed get response with error: %s' % (str(e)))
            raise Exception("failed on getting response data from get response with error message: %s" % (str(e)))


