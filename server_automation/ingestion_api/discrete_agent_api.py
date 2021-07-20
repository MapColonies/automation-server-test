"""
This module wrapping agent api's restful functionality
"""

import logging
# from server_automation.utils import base_requests
from server_automation.configuration import config_ingestion
from server_automation.utils import common
from mc_automation_tools import base_requests
logging.getLogger('server_automation.ingestion_api.discrete_agent_api')


def post_manual_trigger(source_directory):
    """
    This method triggering ingestion process by manual method (from given valid directory
    """
    # todo - add directory inner validator
    body = {'sourceDirectory': source_directory}
    url = common.combine_url(config_ingestion.INGESTION_AGENT_URL, config_ingestion.INGESTION_MANUAL_TRIGGER)
    resp = base_requests.send_post_request(url, body)
    return resp


def get_watching_statuses():
    """
    This method return bool -> true if watcher is on, false if watcher
    """
    url = common.combine_url(config_ingestion.INGESTION_AGENT_URL, config_ingestion.INGESTION_WATCHER_STATUS)
    resp = base_requests.send_get_request(url)
    return resp


def post_start_watch():
    """
    This method change watcher status to true and return -> "watching": true
    """
    url = common.combine_url(config_ingestion.INGESTION_AGENT_URL, config_ingestion.INGESTION_WATCHER_STATUS, config_ingestion.INGESTION_START_WATCHER)
    resp = base_requests.send_post_request(url)
    return resp


def post_stop_watch():
    """
    This method change watcher status to true and return -> "watching": false
    """
    url = common.combine_url(config_ingestion.INGESTION_AGENT_URL, config_ingestion.INGESTION_WATCHER_STATUS, config_ingestion.INGESTION_STOP_WATCHER)
    resp = base_requests.send_post_request(url)
    return resp