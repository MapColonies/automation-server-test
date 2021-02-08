from server_automation.configuration import jira_config

config_dict = jira_config.jira_config_from_json()


def get_jira_config():
    return config_dict
