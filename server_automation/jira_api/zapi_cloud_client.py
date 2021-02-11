# pylint: disable=invalid-name, line-too-long
""" This module wrapping API of zapi client"""
import json
import logging
from urllib.parse import urljoin
import requests
# from zapi_cloud_generator_jwt.util.JWTGenerator import JWTGenerator
from server_automation.jira_api.zapi_cloud_generator_jwt import JWTGenerator

_log = logging.getLogger('server_automation.jira_api.zapi_cloud_client')


class ZAPI_cloud_client:
    """
    This class wrapping zapi for cloud api of jira
    """
    # pylint: disable=too-many-arguments
    def __init__(self,
                 account_id,
                 access_key,
                 secret_key,
                 jwt_exp_in_sec=7200,
                 cloud_base_url="https://prod-api.zephyr4jiracloud.com/connect/"):

        self.account_id = account_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.jwt_exp_in_sec = jwt_exp_in_sec
        self.cloud_base_url = cloud_base_url

    def generate_headers(self, Http_Method, relative_path):
        """ create valid header data for zapi cloud request"""
        # RELATIVE_PATH = (w/o leading and trailing slashes ie "public/rest/api/1.0/...")
        # CANONICAL PATH (Http Method & Relative Path & Query String)
        canonical_path = Http_Method + '&' + "/" + relative_path + '&'

        headers = JWTGenerator(account_id=self.account_id,
                               access_key=self.access_key,
                               secret_key=self.secret_key,
                               canonical_path=canonical_path).headers()

        _log.debug(json.dumps(headers, sort_keys=True, indent=4, separators=(",", ": ")))

        return headers

    def get_general_info(self):
        """ return general info of connection to zapi api"""
        relative_path = "public/rest/api/1.0/config/generalinformation"
        headers = self.generate_headers(Http_Method="GET", relative_path=relative_path)
        url = urljoin(self.cloud_base_url, relative_path)
        _log.debug(url)

        try:
            response = requests.get(
                url=url,
                headers=headers)
        except Exception as e:
            _log.error("error in GET general information with error %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s",msg)

        return res

    # pylint: disable=too-many-arguments
    def create_execution(self, project_id, issue_id, version_id, status, cycleId="-1"):
        """
        Create new execution for test issue - default cycle will be under had-hoc
        """
        relative_path = "public/rest/api/1.0/execution"
        headers = self.generate_headers(Http_Method="POST", relative_path=relative_path)
        request = {"status": status, "projectId": project_id, "issueId": issue_id, "versionId": version_id, "cycleId": cycleId}
        url = urljoin(self.cloud_base_url, relative_path)
        _log.debug(url)
        _log.debug(request)

        try:
            response = requests.post(
                url=url,
                headers=headers, data=json.dumps(request))
        except Exception as e:
            _log.error("error in POST create execution with error %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)['execution']['id']
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res

    def get_issue_executions(self, issue_id, action=None):
        """
        return data of specific issue about his exc. status
        """
        relative_path = "public/rest/api/1.0/executions/search/issue/{}?action={}".format(issue_id, action)

        headers = self.generate_headers(Http_Method="GET",
                                        relative_path="public/rest/api/1.0/executions/search/issue/35868?maxRecords=&expand=&offset"
                                                      "=&action=")
        url = urljoin(self.cloud_base_url, relative_path)
        _log.debug(url)

        try:
            response = requests.get(
                url=url,
                headers=headers)
        except Exception as e:
            _log.error("error in GET executions with error %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res

    # pylint: disable=too-many-arguments
    def update_execution(self, execution_id, project_id, issue_id, version_id, status, cycleId="-1"):
        """ Change issue test about his exc. result according test result"""
        relative_path = "public/rest/api/1.0/execution/{}".format(execution_id)
        headers = self.generate_headers(Http_Method="PUT", relative_path=relative_path)
        url = urljoin(self.cloud_base_url, relative_path)
        _log.debug(url)
        data = {"status": status, "projectId": project_id, "issueId": issue_id, "versionId": version_id, "cycleId": cycleId}

        try:
            response = requests.put(
                url=url,
                headers=headers,
                json=data)
        except Exception as e:
            _log.error("error in PUT update execution with error %s", (str(e)))
            raise e
        res = None
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res
