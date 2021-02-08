import pytest

@pytest.mark.parametrize("issue_id", [(37040)])
def test_when_fail(get_config, Zapi_cloud_client, test_status, issue_id, get_execution):
    assert False

@pytest.mark.parametrize("issue_id", [(37042)])
def test_when_success(get_config, Zapi_cloud_client, test_status, issue_id, get_execution):
    assert True