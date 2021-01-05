from server_automation.exporter_api import storage_utils as su
from server_automation.exporter_api import base_requests as br
from server_automation.utils import common
from server_automation.utils import s3storage as s3
from server_automation.configuration import config
# from geopackage_tools.infra import db_conn as db
from geopackage_tools.validators import validator as gpv
import json
import logging
import os
import time
from datetime import datetime, timedelta

_logger = logging.getLogger("server_automation.function.executors")


def get_task_status(uuid):
    """
    This method provide task status by providing uuid (task id)
    """
    res = su.get_uuid_status(common.combine_url(config.EXPORT_STORAGE_URL, config.STATUSES_API), uuid)
    return res


def send_export_request(request_dict, request_path=None, request_name=None):
    """
    This method send export request of geopackage to trigger service
    :param request_dict: this is dict represent valid request
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
    if request_name:
        request['fileName'] = request_name
    api_url = common.combine_url(config.EXPORT_TRIGGER_URL, config.EXPORT_GEOPACKAGE_API)
    _logger.info('Send request: %s to export with url: %s' % (request['fileName'], api_url))
    resp = br.send_post_request(api_url, request)
    status_code, content = common.response_parser(resp)
    _logger.info('Response of trigger returned with status: %d' % status_code)

    return status_code, content

#deprication
# def send_download_request(subdir, file_name, url=config.DOWNLOAD_STORAGE_URL):
#     """
#     This method send download request for package that was created on shared folder on storage
#     :param url: shared folder uri
#     :param subdir: relative shared folder subdir name
#     :param file_name: geopackage file name
#     :return: status code + response content
#     """
#     api_url = common.combine_url(url, config.DOWNLOAD_API, subdir, '.'.join([file_name, config.PACKAGE_EXT]))
#     _logger.info('Send download request: %s' % api_url)
#     resp = br.send_get_request(api_url)
#     return resp.status_code, resp.content




def send_download_request(pkg_download_url):
    """
    This method send download request for package that was created on shared folder on storage
    :param pkg_download_url: download uri
    :return: status code + response content
    """
    _logger.info('Send download request: %s' % pkg_download_url)
    resp = br.send_get_request(pkg_download_url)
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


def load_gpkg_from_storage(file_name, directory_name):
    if config.S3_EXPORT_STORAGE_MODE:
        s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
        object_key = "/".join([directory_name, ".".join([file_name,config.PACKAGE_EXT])])

        destination_dir = os.path.join(config.S3_DOWNLOAD_DIRECTORY, object_key.split('.')[0])
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        s3_conn.download_from_s3(config.S3_BOCKET_NAME, object_key, os.path.join(destination_dir, destination_dir.split('/')[-1]))
        uri = os.path.join(destination_dir, destination_dir.split('/')[-1])


    else:
        uri = common.combine_url(config.PACKAGE_OUTPUT_DIR, config.EXPORT_DOWNLOAD_DIR_NAME,
                                 ".".join([config.EXPORT_DOWNLOAD_FILE_NAME, config.PACKAGE_EXT]))

    pkg = common.load_file_as_bytearray(uri)
    return pkg

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

        s3_conn.download_from_s3(config.S3_BOCKET_NAME, object_key, os.path.join(destination_dir, destination_dir.split('/')[-1]))
        uri = os.path.join(destination_dir, destination_dir.split('/')[-1])
    else: #FS
        if not os.path.exists(config.PACKAGE_OUTPUT_DIR):
            _logger.error(
                "Output directory not exist [%s]- validate mapping and directory on config" % (config.PACKAGE_OUTPUT_DIR))
            raise Exception("Output directory: [%s] not found ! validate config \ mapping" % (config.PACKAGE_OUTPUT_DIR))

    # TODO fix after environment will be fixed
    # if not os.path.exists(uri):
    #     _logger.error('Package [%s] not exist! file validation failed' % (resp['fileURI'].split('/')[-1:]))
    #     return False

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


def is_geopackage_exist(file_url, request=None, test_name="test name N\A"):
    """
    Validation of specific geopackge on S3\File system
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
        res = s3_conn.is_file_exist(config.S3_BOCKET_NAME, object_key)
        pkg_url = file_url.split('?')[0] if '?' in file_url else file_url # todo - update after download link will be
        return res, pkg_url

    else:
        _logger.info('Test running on file-system mode')
        pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_url.split('/')[-2:]))
        _logger.info(pkg_url)
        res = os.path.exists(pkg_url),
        return res, pkg_url


def get_test_download_url():
    """ This helper method generate and return url of geopackge download - for FS ans OS"""
