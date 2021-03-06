# pylint: disable=invalid-name, broad-except
""" configuration handler for jira api"""
import json
import os
import logging
import server_automation.configuration.config as config

_log = logging.getLogger('server_automation.configuration.jira_config')
FILE_URL = config.FILE_URL


def jira_config_from_json():
    """ Read external config json and parse running memory"""
    file_config = None

    try:
        with open(FILE_URL, 'r') as f:
            file_config = json.load(f)
    except FileNotFoundError as e:
        _log.error(str(e))
        raise e
    except Exception as e2:
        _log.error(str(e2))

    return file_config
