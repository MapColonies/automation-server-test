""" This module responsible of testing export tools - server side:

"""
import pytest
import os
import json
os.environ['DEBUG_LOGS'] = 'True'
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc
from server_automation.configuration import config
from server_automation.utils import common


def test_export_geopackage():
    """ Test case: Export data as valid geoPackages format
        Validate epic 4 – server side – requirement 2
        This test validates that geoPackage includes all tiles and their relative metadata.
    """

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


def test_box_size_limit():
    """This test validate that exporter trigger is limit the bbox size according to configurable param"""
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
    res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
    assert res, print('Error while exporting package')
    exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])


def test_export_on_storage():
    """
    This test validate that package was exported into shared folder properly
    """

    # loading request
    request = request_sampels.get_request_by_box_size(request_sampels.box_size.Sanity)
    assert request, "Error on loading request"
    request = (json.loads(request))
    request['fileName'] = config.EXPORT_DOWNLOAD_FILE_NAME
    request['directoryName'] = config.EXPORT_DOWNLOAD_DIR_NAME

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))
    assert s_code == config.ResponseCode.Ok.value, ('Failed with error code %d - %s' % ( s_code, content))

    # check exporting process and wait till end with results
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, ('Error while exporting package %s' % err)

    # validate file places on storage
    file_location = res['fileURI']
    pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, *(file_location.split('/')[-2:]))
    assert os.path.exists(pkg_url), ("File not exist on storage %s" % pkg_url)

    exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])


def test_download_package():
    #  validate exported file exist on storage from previous test - test_export_on_storage
    pkg_url = common.combine_url(config.PACKAGE_OUTPUT_DIR, config.EXPORT_DOWNLOAD_DIR_NAME,
                                 ".".join([config.EXPORT_DOWNLOAD_FILE_NAME, config.PACKAGE_EXT]))
    assert os.path.exists(pkg_url), print("File not exist on storage %s" % pkg_url)

    #  send and receive download file request
    s_code, downloaded_data = exc.send_download_request(config.EXPORT_DOWNLOAD_DIR_NAME, config.EXPORT_DOWNLOAD_FILE_NAME)
    assert s_code == config.ResponseCode.Ok.value, ("failed download with status code %d" % s_code)

    #  compare downloaded and exported files by hashing
    orig_exported = exc.common.load_file_as_bytearray(pkg_url)  # bytes array
    assert common.generate_unique_fingerprint(orig_exported) == common.generate_unique_fingerprint(downloaded_data), ("download package not equal to exported package")



# test_export_on_storage()
# test_download_package()
# test_export_geopackage()
# test_box_size_limit()
