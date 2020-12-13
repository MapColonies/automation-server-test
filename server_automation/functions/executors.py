from server_automation.exporter_api import storage_utils as su
from server_automation.exporter_api import base_requests as br
from server_automation.utils import common
from server_automation.configuration import config
from geopackage_tools.infra import db_conn as db
from geopackage_tools.validators import validator as gpv
import json
import logging
import os
import time
import datetime

_logger = logging.getLogger("server.executors")


def send_export_request(request_dict, request_path=None):
    """
    This method send export request of geopackage to trigger service
    :param request: this is dict represent valid request
    :param request_path: string
    :return: status http code (int) and response body (dict)
    """
    if request_path:
        try:
            fp = open(request_path, "r")
            _logger.debug("Request: %s ,was loaded successfully" % os.path.basename(request_path))
            request = json.load(fp)
            fp.close()

        except FileNotFoundError as e:
            _logger.error("request json file: %s not exist, please validate location" % request_path)
            raise FileNotFoundError("Failed load file %s with error: $s" % request_path, str(e))
        except Exception as e2:
            _logger.error("Error while trying load request json file: %s" % request_path)
            raise Exception("Failed load file %s with error: %s" % (request_path, str(e2)))

    elif request_dict:
        request = request_dict

    else:
        raise Exception('Unknown error with opening request')

    request = json.loads(request)
    api_url = common.combine_url(config.EXPORT_TRIGGER_URL, config.EXPORT_GEOPACKAGE_API)
    _logger.info('Send request: %s to export with url: %s' % (request['fileName'], api_url))
    resp = br.send_post_request(api_url, request)
    status_code, content = common.response_parser(resp)
    _logger.info('Response of trigger returned with status: %d' % status_code)

    return status_code, content


def send_download_request(subdir, file_name, url=config.DOWNLOAD_STORAGE_URL):
    """
    This method send download request for package that was created on shared folder on storage
    :param url: shared folder uri
    :param subdir: relative shared folder subdir name
    :param file_name: geopackage file name
    :return: status code + response content
    """
    api_url = common.combine_url(url, config.DOWNLOAD_API, subdir, '.'.join([file_name, config.PACKAGE_EXT]))
    _logger.info('Send download request: %s' % api_url)
    resp = br.send_get_request(api_url)
    return resp.status_code, resp.content


def exporter_follower(url, uuid):
    """
    This method follow and ensure specific task progress complete
    :param url: api's url
    :param uuid: task id
    """
    retry_completed = 0
    if not isinstance(uuid, str):
        raise Exception("uuid param type should be string (str)! ")

    t_end = time.time() + config.MAX_EXPORT_RUNNING_TIME
    full_url = common.combine_url(url, config.STATUSES_API)
    running = True
    while running:
        status_code, content = common.response_parser(su.get_uuid_status(full_url, uuid))
        if config.ResponseCode.Ok.value != status_code:
            raise RuntimeError("Error on request status service with error %s:%d" % (
                config.ResponseCode(status_code).name, status_code))

        progress = content['progress']
        if content['status'] == config.EXPORT_STATUS_FAILED:
            raise Exception("Failed on export on task %s" % uuid)
        if progress == 100 and not content['status'] == config.EXPORT_STATUS_COMPLITED:
            time.sleep(10)
            retry_completed += 1
            if retry_completed > 2:
                raise Exception("Error on closing task %s" % uuid)

        current_time = time.time()
        running = not (progress == 100 and content['status'] == config.EXPORT_STATUS_COMPLITED) and current_time < t_end
        _logger.info(
            'Received from task(uuid): %s ,with status code: %d and progress: %d' % (uuid, status_code, progress))

        if current_time > t_end:
            "Got timeout and will stop running progress validation"
            raise Exception("got timeout while following task running")

    _logger.info(
        'Finish exporter job according status index service and file should be places on: %s' % (content['fileURI']))
    results = {
        'taskId': content['taskId'],
        'fileName': content['fileName'],
        'directoryName': content['directoryName'],
        'fileURI': content['fileURI'],
        'expirationTime': content['expirationTime']

    }

    return results


def validate_geo_package(uri):
    """
    This method check if geopackage was created properly. can provide uuid or response
    :param uri: geopackage path
    :return:bool - True if package created ok with relevant content
    """

    if not os.path.exists(config.PACKAGE_OUTPUT_DIR):
        _logger.error(
            "Output directory not exist [%s]- validate mapping and directory on config" % (config.PACKAGE_OUTPUT_DIR))
        raise Exception("Output directory: [%s] not found ! validate config \ mapping" % (config.PACKAGE_OUTPUT_DIR))

        if not os.path.exists(uri):
            _logger.error('Package [%s] not exist! file validation failed' % (resp['fileURI'].split('/')[-1:]))
            return False

    res = gpv.aseert_package(uri)
    return res


def delete_requests(url, requests):
    resp = su.delete_by_uuid(url, requests)
    return resp


def clear_all_tasks(url):
    """
    This method clear db from all tasks, return None if no task on db
    """
    resp = ['db was empty of task']
    statuses = json.loads(su.get_all_statuses(url).text)
    if len(statuses):
        uuids = [stat['taskId'] for stat in statuses]
        resp = su.delete_by_uuid(url, uuids)
    return resp


def create_testing_status(url, directory_name, fileName):
    current_time = datetime.datetime.utcnow()
    current_hour = current_time.hour

    utc_curr = current_time.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
    current_hour = utc_curr.hour


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
        'creationTime': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'),
        'updatedTime': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'),


    }