import json
import os
import sys
root_path = sys.path[1]

FILE_URL = '/home/ronenk1/dev/automation-server-test/jira_config.json'


def jira_config_from_json(file_uri=None):
    file_config = None

    try:
        file_uri = FILE_URL #todo - refactor
        with open(file_uri, 'r') as f:
            file_config = json.load(f)
    except FileNotFoundError as e:
        print(str(e))
        raise e
    except Exception as e2:
        print(str(e2))

    return file_config

