""" This module responsible of testing export tools - server side:

"""
import pytest
import os
import json
import logging
# os.environ['DEV_MODE'] = 'True'
# os.environ['DEBUG_LOGS'] = 'True'
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc
from server_automation.configuration import config
from server_automation.utils import common

_log = logging.getLogger('server_automation.tests.exporter_tool_tests')
uuids = []


def test_export_geopackage():
    """ Test case: Export data as valid geoPackages format
        Validate epic 4 – server side – requirement 2
        This test validates that geoPackage includes all tiles and their relative metadata.
    """

    _log.info(f'Start running test: {test_export_geopackage.__name__}')
    # check and load request json
    request = request_sampels.get_request_sample('et_req_2')
    assert request, \
        f'Test: [{test_export_geopackage.__name__}] Failed: File not exist or failure on loading request json'

    # sending json request and validating export process
    request = json.loads(request)
    request['fileName'] = 'test1_export_geopackage'
    request = json.dumps(request)
    s_code, content = exc.send_export_request(request)
    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_export_geopackage.__name__}] Failed: Exporter trigger return status code [{s_code}] '

    # worker stage - follow exporting via storage statuses API
    try:
        if content.get('uuid'):  # for later system cleanup
            uuids.append(content['uuid'])
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        error_msg = None
    except RuntimeError as e:
        res = None
        error_msg = str(e)
    except Exception as e:
        res = None
        error_msg = str(e)
    assert res, \
        f'Test: [{test_export_geopackage.__name__}] Failed: on follow (worker stage) with message: [{error_msg}]'

    # check geopackage file was created on storage
    file_location = res['fileURI']
    _log.debug(f'File uri expected: {file_location}')

    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)
    # if config.S3_EXPORT_STORAGE_MODE:
    #     _log.info('Test running on s3 mode')
    #     s3_conn = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
    #     assert s3_conn.is_file_exist(config.S3_BOCKET_NAME, ".".join([request['fileName'], config.PACKAGE_EXT])), 'file not exist on s3'
    # else:
    #     _log.info('Test running on file-system mode')
    #     pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_location.split('/')[-2:]))
    #     _log.info(pkg_url)
    assert gpkg_exist, \
        f'Test: [{test_export_geopackage.__name__}] Failed: file not exist on storage [disk \ S3 ]:[{pkg_url}]'

    # validate the package was created properly
    is_valid_package = exc.validate_geo_package(pkg_url)
    assert is_valid_package, \
        f'Test: [{test_export_geopackage.__name__}] Failed: package is corrupted [{pkg_url}]'

    # if config.DEV_MODE and content.get('uuid',None):
    # exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_export_geopackage.__name__)


def test_box_size_limit():
    """ Test case: Export according restricted region size of geoPackage

        Validate epic 4 – server side – requirement 3

        Test creation of geoPackage data, bounded by region size configuration value.
        Default configuration parameter (100X100 according to epic).
        Fail if required region size is greater than this value.
    """

    _log.info('Start running test: %s', test_export_geopackage.__name__)
    err = 'Unknown'

    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Big)
    assert request

    # sending requests with different bbox sizes
    s_code, content = exc.send_export_request(request, request_name="test2_box_size_limit_big")
    assert config.ResponseCode.ValidationErrors.value == s_code and content[
        'name'] == config.BOX_LIMIT_ERROR, "limit box test failed"
    if not os.environ['DEV_MODE']:  # on QA environment the limit size can be changes and its to prevent overload
        request = request_sampels.get_request_by_box_size(request_sampels.box_size.Medium)
        assert request
        s_code, content = exc.send_export_request(request, request_name='test2_box_size_limit_medium')
        assert config.ResponseCode.ValidationErrors.value == s_code and content[
            'name'] == config.BOX_LIMIT_ERROR, "limit box test failed"

    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Sanity)
    assert request
    s_code, content = exc.send_export_request(request, request_name='test2_box_size_limit_small')
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        res = None
        err = str(e)
    assert res, ('Error while exporting package - exporter follow stage %s' % err)
    # exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_box_size_limit.__name__)


# todo - complite test

# def test_delete_old_packages():
#
#     # creating file to test
#     output_dir = config.PACKAGE_OUTPUT_DIR
#     # full_path = os.path.join(output_dir, 'deletion_test', 'delete_test.gpkg')
#     full_path = os.path.join(output_dir, 'e_tests', 'r_short.GPKG')
#
#     try:
#         f = open(full_path, 'r')
#     except Exception:
#         f = None
#
#     assert f, ('File note exist on directory: %s' % full_path)
#     if f:
#         f.close()
#
#     resp, uuid = exc.create_testing_status(output_dir, 'e_tests', 'r_short.GPKG')
#
#     s_code, content = common.response_parser(resp)
#     exc.delete_requests(config.EXPORT_STORAGE_URL, [uuid])
#     assert s_code == config.ResponseCode.Ok.value, content
#     print("On Developing")
#     pass


def test_export_on_storage():
    """ Test case: Package created on shared folder
        Validate epic 4 – server side – requirement 5
        This test validates that geoPackage that was created on storage can be downloaded locally and valid as original
    """
    _log.info('Start running test: %s', test_export_on_storage.__name__)

    # loading request
    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Sanity)
    assert request, \
        f'Test: [{test_export_on_storage.__name__}] Failed: File not exist or failure on loading request json'

    request = (json.loads(request))
    request['fileName'] = config.EXPORT_DOWNLOAD_FILE_NAME
    request['directoryName'] = config.EXPORT_DOWNLOAD_DIR_NAME

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))

    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_export_on_storage.__name__}] Failed: Exporter trigger return status code [{s_code}]'

    # check exporting process and wait till end with results
    res = None
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_export_on_storage.__name__}] Failed: on follow (worker stage) with message: [{err}]'

    # validate file places on storage
    file_location = res['fileURI']
    _log.debug(f'File uri expected: {file_location}')
    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)
    assert gpkg_exist, \
        f'Test: [{test_export_on_storage.__name__}] Failed: file not exist on storage [disk \ S3 ]:[{pkg_url}]'

    # exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_export_on_storage.__name__)


def test_download_package():
    """ Test case: Download locally package from shared storage

        Validate epic 4 – server side – requirement 5

        This test validates that geoPackage that was created on storage can be downloaded locally and valid as original
    """
    _log.info('Start running test: %s', test_export_geopackage.__name__)

    #  validate exported file exist on storage from previous test - test_export_on_storage
    pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, config.EXPORT_DOWNLOAD_DIR_NAME,
                                 ".".join([config.EXPORT_DOWNLOAD_FILE_NAME, config.PACKAGE_EXT]))
    assert os.path.exists(pkg_url), print("File not exist on storage %s" % pkg_url)

    #  send and receive download file request
    s_code, downloaded_data = exc.send_download_request(config.EXPORT_DOWNLOAD_DIR_NAME,
                                                        config.EXPORT_DOWNLOAD_FILE_NAME)
    assert s_code == config.ResponseCode.Ok.value, ("failed download with status code %d" % s_code)

    #  compare downloaded and exported files by hashing
    orig_exported = exc.common.load_file_as_bytearray(pkg_url)  # bytes array
    assert common.generate_unique_fingerprint(orig_exported) == common.generate_unique_fingerprint(downloaded_data), (
        "download package not equal to exported package")

    _log.info('Finish running test: %s', test_download_package.__name__)


def teardown_module(module):
    exc.clear_all_tasks(config.EXPORT_STORAGE_URL)
    print("environment was cleaned up")


# example for future implementation of async tests
# @pytest.mark.asyncio
# async def test_app(create_x, auth):
#     api_client, x_id = create_x
#     resp = await api_client.get(f'my_res/{x_id}', headers=auth)
#     assert resp.status == web.HTTPOk.status_code

# test_delete_old_packages()
# test_export_geopackage()
# test_box_size_limit()
test_export_on_storage()
# test_download_package()
# exc.delete_requests(config.EXPORT_STORAGE_URL, uuids)
