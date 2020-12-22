""" This module responsible of testing export tools - server side:

"""
import pytest
import os
import json
import logging

# os.environ['DEBUG_LOGS'] = 'True'
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc
from server_automation.configuration import config
from server_automation.utils import common

_log = logging.getLogger('server.exporter_tool_tests')


def test_export_geopackage():
    """ Test case: Export data as valid geoPackages format

        Validate epic 4 – server side – requirement 2

        This test validates that geoPackage includes all tiles and their relative metadata.
    """

    _log.info('Start running test: %s', test_export_geopackage.__name__)
    # check and load request json
    request = request_sampels.get_request_sample('et_req_2')
    assert request

    # sending json request and validating export process
    s_code, content = exc.send_export_request(request)
    assert s_code == config.ResponseCode.Ok.value

    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        error_msg = None
    except RuntimeError as e:
        res = None
        error_msg = str(e)
    except Exception as e:
        res = None
        error_msg = str(e)

    assert res, error_msg

    # check geopackage file was created on storage
    file_location = res['fileURI']
    pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_location.split('/')[-2:]))
    assert os.path.exists(pkg_url)

    # validate the package was created properly
    is_valid_package = exc.validate_geo_package(pkg_url)
    assert is_valid_package, print('package is corrupted')

    exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_export_geopackage.__name__)


def test_box_size_limit():
    """ Test case: Export according restricted region size of geoPackage

        Validate epic 4 – server side – requirement 3

        Test creation of geoPackage data, bounded by region size configuration value.
        Default configuration parameter (100X100 according to epic).
        Fail if required region size is greater than this value.
    """

    _log.info('Start running test: %s', test_export_geopackage.__name__)

    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Big)
    assert request
    s_code, content = exc.send_export_request(request)
    assert config.ResponseCode.ValidationErrors.value == s_code and content['name'] == config.BOX_LIMIT_ERROR, print(
        "limit box test failed")
    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Medium)
    assert request
    s_code, content = exc.send_export_request(request)
    assert config.ResponseCode.ValidationErrors.value == s_code and content['name'] == config.BOX_LIMIT_ERROR, print(
        "limit box test failed")

    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Sanity)
    assert request
    s_code, content = exc.send_export_request(request)
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
    except Exception as e:
        res = None
    assert res, ('Error while exporting package - exporter follow stage %s', str(e) )
    exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_export_geopackage.__name__)


def test_delete_old_packages():

    # creating file to test
    output_dir = config.PACKAGE_OUTPUT_DIR
    # full_path = os.path.join(output_dir, 'deletion_test', 'delete_test.gpkg')
    full_path = os.path.join(output_dir, 'e_tests', 'r_short.GPKG')

    try:
        f = open(full_path, 'r')
    except Exception:
        f = None

    assert f, ('File note exist on directory: %s' % full_path)
    if f:
        f.close()

    resp, uuid = exc.create_testing_status(output_dir, 'e_tests', 'r_short.GPKG')

    s_code, content = common.response_parser(resp)
    exc.delete_requests(config.EXPORT_STORAGE_URL, [uuid])
    assert s_code == config.ResponseCode.Ok.value, content
    print("On Developing")
    pass


def test_export_on_storage():
    """ Test case: Package created on shared folder
        Validate epic 4 – server side – requirement 5
        This test validates that geoPackage that was created on storage can be downloaded locally and valid as original
    """
    _log.info('Start running test: %s', test_export_geopackage.__name__)

    # loading request
    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Sanity)
    assert request, "Error on loading request"
    request = (json.loads(request))
    request['fileName'] = config.EXPORT_DOWNLOAD_FILE_NAME
    request['directoryName'] = config.EXPORT_DOWNLOAD_DIR_NAME

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))
    assert s_code == config.ResponseCode.Ok.value, ('Failed with error code %d - %s' % (s_code, content))

    # check exporting process and wait till end with results
    res = None
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, ('Error while exporting package %s' % (err))

    # validate file places on storage
    file_location = res['fileURI']
    pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_location.split('/')[-2:]))
    assert os.path.exists(pkg_url), ("File not exist on storage %s" % pkg_url)

    exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])
    _log.info('Finish running test: %s', test_export_geopackage.__name__)


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

    _log.info('Finish running test: %s', test_export_geopackage.__name__)


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
# test_export_on_storage()
# test_download_package()
# test_export_geopackage()
test_box_size_limit()
