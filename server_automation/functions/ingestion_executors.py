# pylint: disable=line-too-long, invalid-name, fixme
"""This module provide test full functionality """
import json
import logging
import os
from geopackage_tools.validators import validator as gpv
from server_automation.configuration import config_ingestion
from server_automation.ingestion_api import discrete_agent_api
from server_automation.configuration import config
from mc_automation_tools import common as common
from mc_automation_tools import s3storage as s3
_log = logging.getLogger('server_automation.function.ingestion_executors')


def start_manuel_ingestion(path):
    """This method will trigger new process of discrete ingestion by provided path"""
    _log.info(f'Send ingestion request for dir: {path}')
    resp = discrete_agent_api.post_manual_trigger(path)
    status_code = resp.status_code
    content = resp.text
    _log.info(f'receive from agent - manual: status code [{status_code}] and message: [{content}]')
    return status_code, content


def follow_running_task(task_id):
    """This method will follow running ingestion task and return results on finish"""
