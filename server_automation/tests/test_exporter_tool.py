# pylint: disable=line-too-long, invalid-name, broad-except
""" This module responsible of testing export tools - server side:"""
import json
import logging
from server_automation.tests import request_sampels
from server_automation.functions import executors as exc
from server_automation.configuration import config
from server_automation.utils import common
from conftest import ValueStorage

_log = logging.getLogger('server_automation.tests.exporter_tool_tests')
uuids = []


####################################### setup_tests #######################################

###########################################################################################


def test_export_geopackage():
    """ 1. Test case: Exporting Orthophoto (raster data) as geopackage with specific layer
        -----------------------------------------------------------------------------
        Validate requirement 1+2 – server side – 1 Export API
        -----------------------------------------------------------------------------
        This test validates exporting geoPackage includes all tiles and their relative metadata based on best layer.
    """
    _log.info('Start running test: %s', test_export_geopackage.__name__)
    # check and load request json
    request = request_sampels.get_request_sample('et_req_2')
    assert request, \
        f'Test: [{test_export_geopackage.__name__}] Failed: File not exist or failure on loading request json'

    # sending json request and validating export process
    request = json.loads(request)
    request['fileName'] = 'test_case_1_exporter_api'
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
    _log.debug('File uri expected: %s', file_location)

    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)

    assert gpkg_exist, \
        f'Test: [{test_export_geopackage.__name__}] Failed: file not exist on storage [disk | S3 ]:[{pkg_url}]'

    # validate the package was created properly
    is_valid_package = exc.validate_geo_package(pkg_url)
    assert is_valid_package, \
        f'Test: [{test_export_geopackage.__name__}] Failed: package is corrupted [{pkg_url}]'

    # if config.DEV_MODE and content.get('uuid',None):
    # exc.delete_requests(config.EXPORT_STORAGE_URL, [content['uuid']])

    _log.info('Finish running test: %s', test_export_geopackage.__name__)


def test_box_size_limit():
    """ 6. Test case: Export orthophoto according restricted region size (bbox) as geoPackage
        -----------------------------------------------------------------------------
        Validate requirement 12 – server side – 1 Export API
        -----------------------------------------------------------------------------
        Test creation of geoPackage data, bounded by region size configuration value.
        Default configuration parameter (100X100).
        Fail if required region size is greater than this value.
    """

    _log.info('Start running test: %s', test_export_geopackage.__name__)
    err = 'Unknown'

    request = request_sampels.get_request_by_box_size(request_sampels.BoxSize.Big)
    assert request

    # sending requests with different bbox sizes
    s_code, content = exc.send_export_request(request, request_name="test_case_6_exporter_api_big")
    assert config.ResponseCode.ValidationErrors.value == s_code and content[
        'name'] == config.BOX_LIMIT_ERROR, f"limit box [{request_sampels.BoxSize.Medium}] test failed"
    if config.ENVIRONMENT_NAME == 'qa':  # on QA environment the limit size can be changes and its to prevent overload
        request = request_sampels.get_request_by_box_size(request_sampels.BoxSize.Medium)
        assert request
        s_code, content = exc.send_export_request(request, request_name='test_case_6_exporter_api_medium')
        assert config.ResponseCode.ValidationErrors.value == s_code and content[
            'name'] == config.BOX_LIMIT_ERROR, f"limit box [{request_sampels.BoxSize.Medium}] test failed"

    request = request_sampels.get_request_by_box_size(request_sampels.BoxSize.Sanity)
    assert request
    s_code, content = exc.send_export_request(request, request_name='test_case_6_exporter_api_small')
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        res = None
        err = str(e)
    assert res, ('Error while exporting package - exporter follow stage %s' % err)

    _log.info('Finish running test: %s', test_box_size_limit.__name__)


def test_cleanup_gpkg():
    """
        7. Test case: Deletion of old packages after configurable time period
        -----------------------------------------------------------------------------
        Validate requirement 9 – server side – 1 Export API
        -----------------------------------------------------------------------------
        This test check if the system will clear automatically old packages according to configuration value
        (default is 7 days)
    """
    _log.info('Start running test: %s', test_cleanup_gpkg.__name__)
    _log.info('Test %s not implemented for current auto version', test_cleanup_gpkg.__name__)
    _log.info('Finish running test: %s', test_cleanup_gpkg.__name__)


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
    """ 8. Test case: Run export request and create geopackage on shared folder|S3
        -----------------------------------------------------------------------------
        Validate requirement 1 – server side – 1 Export API
        -----------------------------------------------------------------------------
        This test check if the package been exported to configurable directory of shared folder|S3
        and local downloading functionality (depends on worker configuration
    """
    _log.info('Start running test: %s', test_export_on_storage.__name__)

    # loading request
    request = request_sampels.get_request_by_box_size(request_sampels.BoxSize.Sanity)
    assert request, \
        f'Test: [{test_export_on_storage.__name__}] Failed: File not exist or failure on loading request json'

    request = (json.loads(request))
    request['fileName'] = 'test_case_8_exporter_api'
    # request['directoryName'] = config.EXPORT_DOWNLOAD_DIR_NAME

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))

    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_export_on_storage.__name__}] Failed: Exporter trigger return status code [{s_code}]'

    # check exporting process and wait till end with results
    res = None
    try:
        err = "unknown"
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_export_on_storage.__name__}] Failed: on follow (worker stage) with message: [{err}]'

    # validate file places on storage - this is download url
    file_location = res.get('fileURI')
    assert file_location, \
        f'Test: [{test_export_on_storage.__name__}] Failed: download link not exist | created]'
    _log.debug('File uri expected: %s',file_location)
    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)
    assert gpkg_exist, \
        f'Test: [{test_export_on_storage.__name__}] Failed: file not exist on storage [disk | S3 ]:[{pkg_url}]'

    _log.info('Finish running test: %s', test_export_on_storage.__name__)


def test_download_package():
    """ 9. Test case:Download locally orthophoto geopackage from shared storage.
        -----------------------------------------------------------------------------
        Validate requirement 7+11 – server side – 1 Export API
        -----------------------------------------------------------------------------
        This test validates that export process provide download url and able to download locally
    """
    _log.info('Start running test: %s', test_download_package.__name__)

    # Prerequisites - creating export package to test download process
    # prepare request
    request = request_sampels.get_request_by_box_size(request_sampels.BoxSize.Sanity)
    assert request, \
        f'Test: [{test_download_package.__name__}] Failed: File not exist or failure on loading request json'
    request = (json.loads(request))
    request['fileName'] = config.EXPORT_DOWNLOAD_FILE_NAME
    request['directoryName'] = config.EXPORT_DOWNLOAD_DIR_NAME

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))

    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_download_package.__name__}] Failed: Exporter trigger return status code [{s_code}]'

    # check exporting process and wait till end with results
    res = None
    try:
        err = "unknown"
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_download_package.__name__}] Failed: on follow (worker stage) with message: [{err}]'

    # store data for download test
    ValueStorage.gpkg_download_url = res['fileURI']
    ValueStorage.file_name = request['fileName']
    ValueStorage.directory_name = request['directoryName']

    # Test download actual flow
    #  validate exported file exist on storage from previous test - test_export_on_storage
    _log.info(ValueStorage.gpkg_download_url)
    assert ValueStorage.gpkg_download_url, \
        f'Test: [{test_download_package.__name__}] Failed: Download URI not found!]'

    s_code, downloaded_data = exc.send_download_request(ValueStorage.gpkg_download_url)
    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_download_package.__name__}] Failed: Download request failed with status code: [{s_code}])'

    orig_exported = exc.load_gpkg_from_storage(ValueStorage.file_name, ValueStorage.directory_name)
    fp_orig = common.generate_unique_fingerprint(orig_exported)
    fp_downloaded = common.generate_unique_fingerprint(downloaded_data)
    assert fp_orig == fp_downloaded, \
        f'Test: [{test_download_package.__name__}] Failed: download geopackage is not equal to stored: [{fp_orig}]  \
         != [{fp_downloaded}]) '

    _log.info('Finish running test: %s', test_download_package.__name__)


def test_export_by_lod():
    """ 12. Test case: send export request by zoom level (LOD – level of details)
        -----------------------------------------------------------------------------
        Validate requirement 7+11 – server side – 1 Export API
        -----------------------------------------------------------------------------
        This test sending export requests by different max zoom level.
    """
    _log.info('Start running test: %s', test_export_by_lod.__name__)

    request = request_sampels.get_lod_req(request_sampels.ZoomLevels.default)
    assert request, \
        f'Test: [{test_export_by_lod.__name__}] Failed: File not exist or failure on loading request json'
    request = (json.loads(request))
    request['fileName'] = 'test_case_12_exporter_api_ZoomDefault'

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))

    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_export_by_lod.__name__}] Failed: Exporter trigger return status code [{s_code}]'

    # check exporting process and wait till end with results
    res = None
    try:
        err = "unknown"
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_export_by_lod.__name__}] Failed: on follow (worker stage) with message: [{err}]'

    # check geopackage file was created on storage
    file_location = res['fileURI']
    _log.debug('File uri expected: %s', file_location)

    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)

    assert gpkg_exist, \
        f'Test: [{test_export_by_lod.__name__}] Failed: file not exist on storage [disk | S3 ]:[{pkg_url}]'

    # validate the package was created properly
    is_valid_zoom = exc.validate_zoom_level(pkg_url, request['maxZoom'])
    assert is_valid_zoom, \
        f'Test: [{test_export_by_lod.__name__}] Failed: package is corrupted or wrong max zoom data[{pkg_url}]'

    request = request_sampels.get_lod_req(request_sampels.ZoomLevels.med)
    assert request, \
        f'Test: [{test_export_by_lod.__name__}] Failed: File not exist or failure on loading request json'
    request = (json.loads(request))
    request['fileName'] = 'test_case_12_exporter_api_ZoomMed'

    # start trigger export
    s_code, content = exc.send_export_request(json.dumps(request))

    assert s_code == config.ResponseCode.Ok.value, \
        f'Test: [{test_export_by_lod.__name__}] Failed: Exporter trigger return status code [{s_code}]'

    # check exporting process and wait till end with results
    res = None
    try:
        res = exc.exporter_follower(config.EXPORT_STORAGE_URL, content['uuid'])
        uuids.append(content['uuid'])
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_export_by_lod.__name__}] Failed: on follow (worker stage) with message: [{err}]'

    # check geopackage file was created on storage
    file_location = res['fileURI']
    _log.debug('File uri expected: %s', file_location)

    gpkg_exist, pkg_url = exc.is_geopackage_exist(file_location, request=request)

    assert gpkg_exist, \
        f'Test: [{test_export_by_lod.__name__}] Failed: file not exist on storage [disk | S3 ]:[{pkg_url}]'

    # validate the package was created properly
    is_valid_zoom = exc.validate_zoom_level(pkg_url, request['maxZoom'])
    assert is_valid_zoom, \
        f'Test: [{test_export_by_lod.__name__}] Failed: package is corrupted or wrong max zoom data[{pkg_url}]'


def setup_module(module):  # pylint: disable=unused-argument
    """
    This method been executed before test running - env general info
    """
    storage_type = "Object storage" if config.S3_EXPORT_STORAGE_MODE else 'File system'
    _log.info('Current environment of testing:\n Exporter tools service test\nStorage mode: %s\nTesting environment: %s\n'
              , storage_type, config.ENVIRONMENT_NAME)


def teardown_module(module):  # pylint: disable=unused-argument
    """
    This method been executed after test running - env cleaning
    """
    # exc.clear_all_tasks(config.EXPORT_STORAGE_URL) # this function remove all statuses from storage
    exc.delete_requests(config.EXPORT_STORAGE_URL, uuids)
    print("\nenvironment was cleaned up")

# example for future implementation of async tests
# @pytest.mark.asyncio
# async def test_app(create_x, auth):
#     api_client, x_id = create_x
#     resp = await api_client.get(f'my_res/{x_id}', headers=auth)
#     assert resp.status == web.HTTPOk.status_code

# test_delete_old_packages()
test_export_geopackage()
# test_box_size_limit()
# test_export_on_storage()
# test_download_package()
# exc.delete_requests(config.EXPORT_STORAGE_URL, uuids)
# test_export_by_lod()
# exc.delete_requests(config.EXPORT_STORAGE_URL, uuids)
# exc.create_testing_status('hghjg', 'e_tests', 'r_short.GPKG')
