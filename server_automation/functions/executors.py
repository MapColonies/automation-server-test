# pylint: disable=line-too-long, invalid-name, fixme
"""This module provide test full functionality """
import json
import logging
import os
import time
from datetime import datetime, timedelta
from geopackage_tools.validators import validator as gpv
from server_automation.exporter_api import storage_utils as su
# from server_automation.utils import common
# from server_automation.utils import base_requests as br
# from server_automation.utils import s3storage as s3
from server_automation.configuration import config
import server_automation.exporter_api.trigger_api as trigger_api
from mc_automation_tools import common as common
from mc_automation_tools import base_requests as br
from mc_automation_tools import s3storage as s3


_logger = logging.getLogger("server_automation.function.executors")


def get_task_status(uuid):
    """
    This method provide task status by providing uuid (task id)
    """
    res = su.get_uuid_status(common.combine_url(config.EXPORT_STORAGE_URL, config.STATUSES_API), uuid)
    return res


# pylint: disable=raise-missing-from
def send_export_request(request_dict, request_path=None, request_name=None ):
    """
    This method send export request of geopackage to trigger service
    :param request_dict: this is dict represent valid request
    :param request_path: string
    :return: status http code (int) and response body (dict)
    """
    if request_path:
        try:
            fp = open(request_path, "r")
            _logger.debug("Request: %s ,was loaded successfully", os.path.basename(request_path))
            request = json.load(fp)
            fp.close()

        except FileNotFoundError as e:
            _logger.error("request json file: %s not exist, please validate location", request_path)
            raise FileNotFoundError("Failed load file %s with error: $s" % request_path, str(e))
        except Exception as e2:
            _logger.error("Error while trying load request json file: %s", request_path)
            raise Exception("Failed load file %s with error: %s" % (request_path, str(e2)))

    elif request_dict:
        request = request_dict

    else:
        raise Exception('Unknown error with opening request')

    request = json.loads(request)
    if request_name:
        request['fileName'] = request_name
    # api_url = common.combine_url(config.EXPORT_TRIGGER_URL, config.EXPORT_GEOPACKAGE_API)
    # _logger.info('Send request: %s to export with url: %s', request['fileName'], api_url)
    _logger.info('Send request: %s to export ', request['fileName'])
    # resp = br.send_post_request(api_url, request)
    trigger = trigger_api.ExporterTrigger()
    resp = trigger.post_exportGeopackage(request)
    status_code, content = common.response_parser(resp)
    _logger.info('Response of trigger returned with status: %d', status_code)

    return status_code, content


def send_download_request(pkg_download_url):
    """
    This method send download request for package that was created on shared folder on storage
    :param pkg_download_url: download uri
    :return: status code + response content
    """
    _logger.info('Send download request: %s', pkg_download_url)
    resp = br.send_get_request(pkg_download_url)
    return resp.status_code, resp.content


# todo - refactor more generic with follower method
def get_single_export_state(uuid):
    """
    This method return single export task's state
    """
    trigger = trigger_api.ExporterTrigger()
    response_dict, status_code = trigger.get_status_by_uuid(uuid)
    progress = response_dict['progress']
    status = response_dict['status']
    if config.ResponseCode.Ok.value != status_code:
        raise RuntimeError("Error on request status service with error %s:%d" % (
            config.ResponseCode(status_code).name, status_code))

    if status == config.EXPORT_STATUS_FAILED:
        raise Exception("Failed on export on task %s" % uuid)
    return status, progress


# def exporter_follower(url, uuid):
def exporter_follower(uuid):
    """
    This method follow and ensure specific task progress complete
    :param uuid: task id
    """
    trigger = trigger_api.ExporterTrigger()
    retry_completed = 0
    if not isinstance(uuid, str):
        raise Exception("uuid param type should be string (str)! ")

    t_end = time.time() + config.MAX_EXPORT_RUNNING_TIME
    # full_url = common.combine_url(url, config.STATUSES_API)
    running = True
    while running:

        # # status_code, content = common.response_parser(su.get_uuid_status(full_url, uuid))
        # response_dict = trigger.get_status_by_uuid(uuid)
        # status_code = response_dict['progress']
        # content = response_dict['status']
        # # status_code, content = common.response_parser(trigger.get_status_by_uuid(uuid))
        # if config.ResponseCode.Ok.value != status_code:
        #     raise RuntimeError("Error on request status service with error %s:%d" % (
        #         config.ResponseCode(status_code).name, status_code))
        #
        # progress = content['progress']
        # if content['status'] == config.EXPORT_STATUS_FAILED:
        #     raise Exception("Failed on export on task %s" % uuid)
        # if progress == 100 and not content['status'] == config.EXPORT_STATUS_COMPLITED:
        #     time.sleep(10)
        #     retry_completed += 1
        #     if retry_completed > 2:
        #         raise Exception("Error on closing task %s" % uuid)
        #
        # current_time = time.time()
        # running = not (progress == 100 and content['status'] == config.EXPORT_STATUS_COMPLITED) and current_time < t_end
        # _logger.info(
        #     'Received from task(uuid): %s ,with status code: %d and progress: %d', uuid, status_code, progress)

        # status_code, content = common.response_parser(su.get_uuid_status(full_url, uuid))
        response_dict, status_code = trigger.get_status_by_uuid(uuid)
        progress = response_dict['progress']
        status = response_dict['status']
        # status_code, content = common.response_parser(trigger.get_status_by_uuid(uuid))
        if config.ResponseCode.Ok.value != status_code:
            raise RuntimeError("Error on request status service with error %s:%d" % (
                config.ResponseCode(status_code).name, status_code))

        if status == config.EXPORT_STATUS_FAILED:
            raise Exception("Failed on export on task %s" % uuid)
        if progress == 100 and not status == config.EXPORT_STATUS_COMPLITED:
            time.sleep(10)
            retry_completed += 1
            if retry_completed > 2:
                raise Exception("Error on closing task %s" % uuid)

        current_time = time.time()
        running = not (progress == 100 and status == config.EXPORT_STATUS_COMPLITED) and current_time < t_end
        _logger.info(
            'Received from task(uuid): %s ,with status code: %d and progress: %d', uuid, status_code, progress)

        if current_time > t_end:
            _logger.error("Got timeout and will stop running progress validation")
            raise Exception("got timeout while following task running")

    _logger.info(
        'Finish exporter job according status index service and file should be places on: %s', (response_dict['link']))
    results = {
        'taskId': response_dict['taskId'],
        'fileName': response_dict['fileName'],
        'directoryName': response_dict['directoryName'],
        'fileURI': response_dict['link'],
        'expirationTime': response_dict['expirationTime']

    }

    return results


def load_gpkg_from_storage(file_name, directory_name):
    """
    - This function load to memory geopackage by provided name
    - Its support FS and OS by running configuration
    """
    if config.S3_EXPORT_STORAGE_MODE:
        s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
        object_key = "/".join([directory_name, ".".join([file_name, config.PACKAGE_EXT])])

        destination_dir = os.path.join(config.S3_DOWNLOAD_DIRECTORY, object_key.split('.')[0])
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        s3_conn.download_from_s3(config.S3_BUCKET_NAME, object_key, os.path.join(destination_dir, destination_dir.split('/')[-1]))
        uri = os.path.join(destination_dir, destination_dir.split('/')[-1])


    else:
        uri = common.combine_url(config.PACKAGE_OUTPUT_DIR, config.EXPORT_DOWNLOAD_DIR_NAME,
                                 ".".join([config.EXPORT_DOWNLOAD_FILE_NAME, config.PACKAGE_EXT]))

    pkg = common.load_file_as_bytearray(uri)
    return pkg


def validate_zoom_level(uri, max_zoom_level):
    """ check if current geopackage provide only zoom that restricted by provided zoom level value"""
    s_code, downloaded_data = send_download_request(uri)
    if config.ResponseCode.Ok.value != s_code:
        raise ConnectionError('Failed on downloading data')
    file_name = os.path.basename(uri)
    download_local_url = common.combine_url(config.TMP_DIR, "_".join(["zoom", str(max_zoom_level)]))
    full_location = common.combine_url(download_local_url, file_name)
    if not os.path.exists(download_local_url):
        os.makedirs(download_local_url)
    with open(full_location, "wb") as f:
        f.write(downloaded_data)
    # if config.S3_EXPORT_STORAGE_MODE:
    #     s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
    #     object_key = "/".join(uri.split("/")[-2:])
    #
    #     destination_dir = os.path.join(config.S3_DOWNLOAD_DIRECTORY, object_key.split('.')[0])
    #     if not os.path.exists(destination_dir):
    #         os.makedirs(destination_dir)
    #
    #     s3_conn.download_from_s3(config.S3_BUCKET_NAME, object_key, os.path.join(destination_dir, destination_dir.split('/')[-1]))
    #     uri = os.path.join(destination_dir, destination_dir.split('/')[-1])
    # else:  # FS
    #     if not os.path.exists(config.PACKAGE_OUTPUT_DIR):
    #         _logger.error(
    #             "Output directory not exist [%s]- validate mapping and directory on config", config.PACKAGE_OUTPUT_DIR)
    #         raise Exception("Output directory: [%s] not found ! validate config or mapping" % config.PACKAGE_OUTPUT_DIR)
    res = gpv.validate_zoom_levels(full_location, max_zoom_level)
    res = set(res)
    return max(res) <= max_zoom_level


def validate_geo_package(uri):
    """
    This method check if geopackage was created properly. can provide uuid or response
    :param uri: geopackage path
    :return:bool - True if package created ok with relevant content
    """
    if config.S3_EXPORT_STORAGE_MODE:
        s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
        object_key = "/".join(uri.split("/")[-2:])

        destination_dir = os.path.join(config.S3_DOWNLOAD_DIRECTORY, object_key.split('.')[0])
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        s3_conn.download_from_s3(config.S3_BUCKET_NAME, object_key, os.path.join(destination_dir, destination_dir.split('/')[-1]))
        uri = os.path.join(destination_dir, destination_dir.split('/')[-1])
    else:  # FS
        if not os.path.exists(config.PACKAGE_OUTPUT_DIR):
            _logger.error(
                "Output directory not exist [%s]- validate mapping and directory on config", config.PACKAGE_OUTPUT_DIR)
            raise Exception("Output directory: [%s] not found ! validate config | mapping" % config.PACKAGE_OUTPUT_DIR)


    res = gpv.aseert_package(uri)
    return res


def delete_requests(url, requests):
    """ use storage wrapper of api to delete request by their uuid"""
    resp = su.delete_by_uuid(url, requests)
    return resp


def clear_all_tasks(url):
    """
    This method clear db from all tasks, return None if no task on db
    """
    resp = ['db was empty of task']
    statuses = json.loads(su.get_all_statuses(url).text)
    if statuses and len(statuses) > 0:
        uuids = [stat['taskId'] for stat in statuses]
        resp = su.delete_by_uuid(url, uuids)
    return resp


# pylint: disable=no-else-return
def create_testing_status(directory_name, fileName):
    """ mock helper function that create status on storage"""
    current_time = datetime.utcnow()
    utc_curr = current_time.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
    utc_expierd = (current_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%SZ')

    body = {
        'taskId': common.generate_uuid(),
        'userId': 'deletion_test',
        'fileName': fileName.split('.')[0],
        'directoryName': directory_name,
        'fileURI': common.combine_url(config.DOWNLOAD_STORAGE_URL, config.DOWNLOAD_API, directory_name, fileName),
        'progress': 100,
        'sourceLayer': config.SOURCE_LAYER,
        'status': config.EXPORT_STATUS_COMPLITED,
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        34.8119380171075,
                        31.9547503375918
                    ],
                    [
                        34.822372617076,
                        31.9547503375918
                    ],
                    [
                        34.822372617076,
                        31.9642696217735
                    ],
                    [
                        34.8119380171075,
                        31.9642696217735
                    ], [
                    34.8119380171075,
                    31.9547503375918
                ]
                ]
            ]
        },
        'estimatedFileSize': 1500,
        'realFileSize': 1500,
        'creationTime': utc_curr,
        'updatedTime': utc_curr,
        'expirationTime': utc_expierd,

    }

    resp = br.send_post_request(common.combine_url(config.EXPORT_STORAGE_URL, config.STATUSES_API), body)
    if resp.status_code == config.ResponseCode.Ok.value:
        _logger.info('Created new task with uuid: %s', (body['taskId']))
        _logger.debug('Task was registered as : body %s', body)
        return resp, body['taskId']
    else:
        _logger.error('Error while trying create new task with - status: %d | error: %s', resp.status_code, resp.content)
        return resp, "None"


# pylint: disable=no-else-return
def is_geopackage_exist(file_url, request=None):
    """
    Validation of specific geopackge on S3 or File system
    """
    if config.S3_EXPORT_STORAGE_MODE:
        _logger.info('Test running on s3 mode')
        try:
            s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
        except Exception as e:
            _logger.error('Some error occur one connection to S3')
            raise e
        if isinstance(request, str):
            request = json.loads(request)
        object_key = ".".join([request['fileName'], config.PACKAGE_EXT])
        object_key = "/".join([request['directoryName'], object_key])
        res = s3_conn.is_file_exist(config.S3_BUCKET_NAME, object_key)
        pkg_url = file_url.split('?')[0] if '?' in file_url else file_url  # todo - update after download link will be
        return res, pkg_url

    else:
        _logger.info('Test running on file-system mode')
        pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_url.split('/')[-2:]))
        _logger.info(pkg_url)
        res = os.path.exists(pkg_url)
        return res, pkg_url


def get_test_download_url():
    """ This helper method generate and return url of geopackge download - for FS ans OS"""
