"""This module provide basic sanity test running to test deployment of exporter services"""
import json
import logging
from datetime import datetime

from server_automation.configuration import config, config_dev
from mc_automation_tools import common, s3storage, bash_utils
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc
from server_automation.functions import environment_validators
_log = logging.getLogger('server_automation.tests.ci_cd')
Z_TIME = datetime.now().strftime('_%Y%m_%d_%H_%M_%S')


def get_status_message(s_code):
    message = 'Unknown error'
    if s_code == config.ResponseCode.Ok.value:
        message = config.ResponseCode.Ok.name
    elif s_code == config.ResponseCode.ValidationErrors.value:
        message = config.ResponseCode.ValidationErrors.name
    elif s_code == config.ResponseCode.StatusNotFound.value:
        message = config.ResponseCode.StatusNotFound.name
    elif s_code == config.ResponseCode.ServerError.value:
        message = config.ResponseCode.ServerError.name
    elif s_code == config.ResponseCode.DuplicatedError.value:
        message = config.ResponseCode.DuplicatedError.name
    elif s_code == config.ResponseCode.GetwayTimeOut.value:
        message = config.ResponseCode.GetwayTimeOut.name
    return message


def test_environment_validation():
    """This test validate basic pre-running validation of exporter environment micro-services"""

    # fields to test:
    exporter_ui = config_dev.EXPORT_UI_URL
    trigger_api = common.combine_url(config_dev.EXPORT_TRIGGER_URL, config.GET_EXPORT_STATUSES_API)
    map_proxy = config_dev.MAP_PROXY_URL
    s3_end_point = config_dev.S3_END_POINT
    s3_access_key = config_dev.S3_ACCESS_KEY
    s3_secret_key = config_dev.S3_SECRET_KEY
    s3_bucket_name = config_dev.S3_BUCKET_NAME
    postgress_vm = config_dev.POSTGRESS_VM

    _log.info('Pre - Running test series that validate environment:\n'
              'Will check :\n'
              f'    1) Exporter ui - {exporter_ui}\n'
              f'    2) Trigger API - {trigger_api}\n'
              f'    3) Map_proxy - {map_proxy}\n'
              f'    4) S3 client - End point: {s3_end_point}, Bucket: {s3_bucket_name}\n'
              f'    5) Postgress - VM alive : address: {postgress_vm}\n'
              f'    6) ELK - VM - kafka service')
    ui_ok = common.check_url_exists(exporter_ui, config.HTTP_REQ_TIMEOUT)
    trigger_ok = common.check_url_exists(trigger_api, config.HTTP_REQ_TIMEOUT)
    map_proxy_ok = common.check_url_exists(map_proxy, config.HTTP_REQ_TIMEOUT)
    s3_ok = s3storage.check_s3_valid(s3_end_point, s3_access_key, s3_secret_key, s3_bucket_name)
    postgress_vm_ok = common.ping_to_ip(postgress_vm)
    ssh_conn = bash_utils.ssh_to_machine(postgress_vm, config_dev.AZURE_USER_NAME, config_dev.AZURE_PASSWORD)
    if ssh_conn:
        postgress_vm_ok = environment_validators.is_postgress_alive(ssh_conn)




    pass


def test_sanity_export_e2e():
    """
    This test provide End-To-End exporting process of geopackage and use all functionality to validate deployment
    environment was set properly
    """
    _log.info('Start running test: %s', test_sanity_export_e2e.__name__)
    # check and load request json
    request = request_sampels.get_request_sample('_req_ci_cd')
    assert request, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: File not exist or failure on loading request json'
    # sending json request and validating export process
    request = json.loads(request)
    request['fileName'] = 'ci_cd_test' + Z_TIME
    request = json.dumps(request)
    s_code, content = exc.send_export_request(request)
    message = get_status_message(s_code)
    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: Exporter trigger return status code [{s_code}] and content: [{message}] '

    # worker stage - follow exporting via storage statuses API
    try:
        res = exc.exporter_follower(content['uuid'])
        error_msg = None
    except RuntimeError as e:
        res = None
        error_msg = str(e)
    except Exception as e:
        res = None
        error_msg = str(e)
    assert res, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: on follow (worker stage) with message: [{error_msg}]'

    # check geopackage file was created on storage
    file_location = res['fileURI']
    _log.debug('File uri expected: %s', file_location)

    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)

    assert gpkg_exist, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: file not exist on storage [disk | S3 ]:[{pkg_url}]'

    # validate the package was created properly
    is_valid_package = exc.validate_geo_package(pkg_url)
    assert is_valid_package, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: package is corrupted [{pkg_url}]'

    _log.info('Finish running test: %s', test_sanity_export_e2e.__name__)


# test_sanity_export_e2e()
test_environment_validation()