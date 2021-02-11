# pylint: disable=invalid-name, line-too-long
"""This module wrapping and provide access into jira's cloud client API"""
import json
import logging
from urllib.parse import urljoin
import requests
from requests.auth import HTTPBasicAuth


_log = logging.getLogger('server_automation.jira_api.jira_cloud_client')


class Jira_Cloud_Client:
    """ This class create jira cloud connected object by credential from configuration"""
    def __init__(self, user_email, user_API_token, base_url):
        self.user_email = user_email
        self.user_API_token = user_API_token
        self.base_url = base_url

        self.auth = HTTPBasicAuth(self.user_email, self.user_API_token)
        self.headers = {"Accept": "application/json"}

    def get_current_user(self):
        """ Return details with which user connected to API """
        url = urljoin(self.base_url, "/rest/api/3/myself")
        try:
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                auth=self.auth
            )

        except Exception as e:
            _log.error("error in GET user with message %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res

    def get_current_user_id(self):
        """ Return details with which user id connected to API"""
        user = self.get_current_user()
        res = None
        if user is not None:
            res = user["accountId"]

        return res

    def get_project_by_key(self, project_key):
        """ This return project data by providing key"""
        url = urljoin(self.base_url, "/rest/api/3/project/{}".format(project_key))
        try:
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                auth=self.auth
            )

        except Exception as e:
            _log.error("error in GET project with message %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res

    def get_project_id_with_key(self, project_key):
        """ get project id according project key"""
        project = self.get_project_by_key(project_key)

        res = None
        if project is not None:
            res = int(project["id"])

        return res

    def get_issue_by_key(self, issue_key):
        """ return issue by key providing"""
        url = urljoin(self.base_url, "/rest/api/3/issue/{}".format(issue_key))
        try:
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                auth=self.auth
            )

        except Exception as e:
            _log.error("error in GET issue with message %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res

    def get_issue_id_by_key(self, issue_key):
        """ return issue by his key"""
        issue = self.get_issue_by_key(issue_key)

        res = None
        if issue is not None:
            res = int(issue["id"])

        return res

    def get_all_issues_in_project_with_type(self, project_key, issue_type):
        """ return all issues by type and project key"""
        url = urljoin(self.base_url, "/rest/api/3/search")

        query = {
            'jql': 'project = {} and issuetype = {}'.format(project_key, issue_type),
            'fields': ["summary", "customfield_10006"],
            'maxResults': 10000
        }

        try:
            response = requests.request(
                "GET",
                url,
                headers=self.headers,
                auth=self.auth,
                params=query
            )

        except Exception as e:
            _log.error("error in GET all issues with type with message %s", str(e))
            raise e

        res = None
        if response.status_code == requests.codes.ok:   # pylint: disable=no-member
            res = json.loads(response.text)
        else:
            msg = ",".join([str(response.reason), str(response.text)])
            _log.error("did not return successfully with message %s", msg)

        return res
