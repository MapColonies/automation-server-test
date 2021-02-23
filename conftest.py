import pytest
import logging
import datetime
from server_automation.configuration import config

if config.USE_JIRA:
    from server_automation.configuration import jira_config
    from server_automation.jira_api.jira_cloud_client import Jira_Cloud_Client
    from server_automation.jira_api.zapi_cloud_client import ZAPI_cloud_client

_log = logging.getLogger('server_automation.conftest')


class ValueStorage:
    gpkg_download_url = None
    file_name = None
    directory_name = None


STATUS = {
    "pass": {"id": 1},
    "fail": {"id": 2},
    "unexecuted": {"id": -1}
}


@pytest.fixture(scope="function", autouse=False)
def Zapi_cloud_client(get_config):
    zapi_cloud_client_instace = ZAPI_cloud_client(account_id=get_config["account_id"],
                                                  access_key=get_config["access_key"],
                                                  secret_key=get_config["secret_key"],
                                                  jwt_exp_in_sec=get_config["jwt_exp_in_sec"],
                                                  cloud_base_url=get_config["cloud_base_url"])

    yield zapi_cloud_client_instace


@pytest.fixture(scope="function", autouse=False)
def get_execution(request, get_config, Zapi_cloud_client, issue_id):
    version_id = get_config["version_id"]
    project_id = get_config["project_id"]
    cycleId = get_config["cycleId"]
    execution_id = Zapi_cloud_client.create_execution(project_id=project_id,
                                                      issue_id=issue_id,
                                                      version_id=version_id,
                                                      status=STATUS["unexecuted"],
                                                      cycleId=cycleId)
    yield

    if request.node.rep_setup.failed:
        _log.error('error in setUp, please check log errors and fix them before trying again')
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            status = Zapi_cloud_client.update_execution(execution_id=execution_id, project_id=project_id, issue_id=issue_id,
                                                        version_id=version_id, status=STATUS["fail"], cycleId=cycleId)
            if status is not None:
                _log.debug("TEST {} JIRA update SUCCESS".format(request.node.nodeid))
        else:
            status = Zapi_cloud_client.update_execution(execution_id=execution_id, project_id=project_id, issue_id=issue_id,
                                                        version_id=version_id, status=STATUS["pass"], cycleId=cycleId)
            if status is not None:
                _log.debug("TEST {} JIRA update SUCCESS".format(request.node.nodeid))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


#
# @pytest.fixture(scope="function", autouse=False)
# def get_function_name():
#     time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
#     function_name = get_function_name_from_env() + "_" + time
#
#     return function_name

# @pytest.fixture(scope="function", autouse=False)
# def get_log(get_function_name):
#     Path(TEST_LOGGER_FOLDER).mkdir(parents=True, exist_ok=True)
#     time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
#     logger_name = get_function_name
#     test_logger = setUp_Log(logger_name, logging.DEBUG, TEST_LOGGER_FOLDER)
#     test_logger.debug("initializing setUp operations for test {} at ".format(get_function_name, time))
#     yield test_logger
#     test_logger.debug("finalizing tearDown operations for test at {}".format(get_function_name, time))


@pytest.fixture(scope="function", autouse=False)
def get_config():
    config = jira_config.jira_config_from_json()
    yield config


@pytest.fixture(scope="function", autouse=False)
def test_status(request):
    _log.debug("*" * 41 + 'TEST BODY' + "*" * 41)
    yield
    if request.node.rep_setup.failed:
        _log.error('error in setUp, please check log errors and fix them before trying again')
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            _log.debug("TEST {} FAILED".format(request.node.nodeid))
        else:
            _log.debug("TEST {} PASSED".format(request.node.nodeid))

    _log.debug("*" * 39 + 'TEST_TEARDOWN' + "*" * 39)
