import json
import pytest

from server_automation.jira_api.jira_cloud_client import Jira_Cloud_Client

TOKEN = "4v3yMMqsKwwPY49bjmQo274C"
ACCOUNT_ID = "5f7633e0e31b69006f962ed1"
URL = "https://rnd-hub.atlassian.net/"
USER_MAIL = "ronenk1@rnd-hub.com"
BASE_URL = "https://rnd-hub.atlassian.net/"
OUTPUT_FILE = "/home/ronenk1/dev/automation-server-test/jira_issues.json"


# @pytest.mark.parametrize("account_id", [(ACCOUNT_ID)])
# def test_jira_self(account_id):
#     jira_cloud_client = Jira_Cloud_Client(user_email=USER_MAIL, user_API_token=TOKEN, base_url=BASE_URL)
#
#     user = jira_cloud_client.get_current_user()
#     print(user)
#     assert user != None


# @pytest.mark.parametrize("issue_key, issue_id", [("MAPCO-266", 37040)])
# def test_get_issue_by_key(issue_key, issue_id):
#     jira_cloud_client = Jira_Cloud_Client(user_email=USER_MAIL, user_API_token=TOKEN,
#                                           base_url=BASE_URL)
#
#     issue = jira_cloud_client.get_issue_by_key(issue_key=issue_key)
#
#     print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
#     assert issue == 37040
# #
# @pytest.mark.parametrize("account_id", [(ACCOUNT_ID)])
# def test_jira_self_id(jira_cloud_client, account_id):
#     # jira_cloud_client = Jira_Cloud_Client(user_email=USER_MAIL, user_API_token=TOKEN,
#     #                                       base_url=BASE_URL)
#
#     user_id = jira_cloud_client.get_current_user_id()
#
#     assert account_id == user_id
#

# @pytest.mark.parametrize("project_key, project_id", [("TSIN", 10149)])
# def test_get_project_by_key(jira_cloud_client, project_key, project_id):
#     # jira_cloud_client = Jira_Cloud_Client(user_email=USER_MAIL, user_API_token=TOKEN,
#     #                                       base_url=BASE_URL)
#
#     project = jira_cloud_client.get_project_by_key(project_key=project_key)
#
#     assert project != None


@pytest.mark.parametrize("project_key, issue_type", [("MAPCO", "Test")])
def test_get_all_project_issues_with_type(project_key, issue_type):
    jira_cloud_client = Jira_Cloud_Client(user_email=USER_MAIL, user_API_token=TOKEN,
                                          base_url=BASE_URL)

    print(jira_cloud_client.get_project_id_with_key('MAPCO'))

    ret_project_issues = jira_cloud_client.get_all_issues_in_project_with_type(project_key=project_key, issue_type=issue_type)

    # print(json.dumps(ret_project_issues, sort_keys=True, indent=4, separators=(",", ": ")))

    with open(file=OUTPUT_FILE, mode="w", encoding="utf-8") as file:
        file.write(json.dumps(ret_project_issues, sort_keys=True, indent=4, separators=(",", ": ")).replace("customfield_10006", "Epic"))