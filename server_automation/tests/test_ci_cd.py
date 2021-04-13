"""This module provide basic sanity test running to test deployment of exporter services"""
import json
import logging
import os
from datetime import datetime

from server_automation.configuration import config
from mc_automation_tools import common as common
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc

_log = logging.getLogger('server_automation.tests.ci_cd')
Z_TIME = datetime.now().strftime('_%Y%m_%d_%H_%M_%S')


### Environment Variables ###
def variabels_setter():
    config.EXPORT_TRIGGER_URL = os.environ.get('EXPORTER_TRIGGER_API',
                                               "https://trigger-raster.apps.v0h0bdx6.eastus.aroapp.io")
    config.OPENSHIFT_DEPLOY = common.get_environment_variable('OPENSHIFT_DEPLOY', True)
    config.MAX_EXPORT_RUNNING_TIME = common.get_environment_variable('MAX_EXPORT_RUNNING_TIME', 5) * 60
    config.S3_EXPORT_STORAGE_MODE = common.get_environment_variable('S3_EXPORT_STORAGE_MODE', True)
    config.S3_END_POINT = os.environ.get('S3_END_POINT')
    config.S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
    config.S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
    config.S3_BUCKET_NAME = common.get_environment_variable('S3_BUCKET_NAME', None)
    config.S3_DOWNLOAD_DIRECTORY = common.get_environment_variable('S3_DOWNLOAD_DIR', '/tmp/')


def test_sanity_export_e2e():
    """
    This test provide End-To-End exporting process of geopackage and use all functionality to validate deployment
    environment was set properly
    """
    variabels_setter()
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
    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_sanity_export_e2e.__name__}] Failed: Exporter trigger return status code [{s_code}] and content [{content}] '

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
