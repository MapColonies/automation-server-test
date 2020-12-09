from . import base_requests as conn
from server_automation.utils import common
from server_automation.configuration import config
import json


def get_all_statuses(url):
    """
    This method return all statuses on db
    :param url: api's url
    :return: list[dict]
    """
    full_url = common.combine_url(url, config.STATUSES_API)
    resp = conn.send_get_request(full_url)
    return resp


def get_uuid_status(url, uuid):
    """This method return current state of export task by uuid created"""
    full_url = common.combine_url(url, uuid)
    resp = conn.send_get_request(full_url)
    return resp


def delete_by_uuid(url, uuid):
    """
    This delete from common storage db the status of specific uuid given as list
    :param url: api's url
    :param uuid: list of strings represent uuid of task to delete
    :return: status request response type
    """
    full_url = common.combine_url(url, config.STATUSES_API, config.DELETE_API)
    resp = conn.send_post_request(full_url, uuid)
    return resp

def create_testing_status(url, directory_name, fileName):
    body = {
        'userId': 'deletion_test',
        'fileName': fileName.split('.')[0],
        'directoryName': directory_name,
        'fileURI': common.combine_url(config.DOWNLOAD_STORAGE_URL, config.DOWNLOAD_API, directory_name, fileName),
        'progress': 100,
        'status': config.EXPORT_STATUS_COMPLITED,
        "geometry": {
            "type": "Point",
            "coordinates": [
                125.6,
                10.1
            ]
        },
        'estimatedFileSize': 1500,
        'realFileSize': 1500,
        'creationTime': 222,

    }



# def clear_all_tasks(url):
#     """
#     This method clear db from all tasks, return None if no task on db
#     """
#     uuids = None
#     statuses = json.loads(get_all_statuses(url).text)
#     if len(statuses):
#         uuids = [stat['taskId'] for stat in statuses]
#         resp = delete_by_uuid(url, uuids)
#     return resp