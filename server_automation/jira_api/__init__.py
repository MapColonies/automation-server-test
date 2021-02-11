# pylint: disable=line-too-long
""" This module init the configuration for jira api's based of outer source file for config and credential """
from server_automation.configuration import jira_config

config_dict = jira_config.jira_config_from_json()


def get_jira_config():
    """
    Return jira's configuration dictionary
    """
    return config_dict
