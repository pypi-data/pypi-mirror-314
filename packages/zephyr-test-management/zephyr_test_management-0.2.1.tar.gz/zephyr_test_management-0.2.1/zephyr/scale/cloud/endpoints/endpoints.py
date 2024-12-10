from typing import Union
from zephyr.common.cloud.endpoints import EndpointTemplate, TestCaseEndpoints, IssueLinksEndpoints
from .paths import ScaleCloudPaths as Paths


class ScaleTestCaseEndpoints(TestCaseEndpoints):
    """
    Api wrapper for "Test Case" endpoints

    Details: https://support.smartbear.com/zephyr-scale-cloud/api-docs/#tag/Test-Cases
    """

    def get_versions(self, test_case_key: str, **kwargs):
        """
        Returns all test case versions for a test case with specified key.
        Response is ordered by most recent first
        """
        return self.session.get_paginated(Paths.CASE_VERS.format(test_case_key),
                                          params=kwargs)

    def get_version(self, test_case_key: str, version: str):
        """Retrieves a specific version of a test case."""
        return self.session.get(Paths.CASE_VER.format(test_case_key, version))

class TestPlanEndpoints(EndpointTemplate):
    """Api wrapper for "Test Plan" endpoints"""

    def get_test_plans(self, **kwargs):
        """Retrieves all test plans. Query parameters can be used to filter the results.

        Keyword arguments:
        :keyword projectKey: Jira project key filter
        :keyword maxResults: A hint as to the maximum number of results to return in each call
        :keyword startAt: Zero-indexed starting position. Should be a multiple of maxResults
        :return: dict with response body
        """
        return self.session.get_paginated(Paths.PLANS, params=kwargs)

    def create_test_plan(self, project_key: str, name: str, **kwargs):
        """Creates a test plan. All required test plan custom fields
         should be present in the request.

        :param project_key: Jira project key
        :param name: test plan name
        :return: dict with response body
        """
        json = {"projectKey": project_key,
                "name": name}
        json.update(kwargs)
        return self.session.post(Paths.PLANS, json=json)

    def get_test_plan(self, test_plan_key: Union[str, int]):
        """
        Returns a test plan for the given id or key.

        :param test_plan_key: The ID or key of the test plan
        :return: dict with response body
        """
        return self.session.get(Paths.PLAN_KEY.format(test_plan_key))

    def create_web_links(self, test_plan_key: Union[str, int], url: str, description: str):
        """
        Creates a link between a test plan and a generic URL.

        :param test_plan_key: The ID or key of the test plan
        :param url: The web link URL
        :param description: The link description
        :return: dict with response body
        """
        json = {"url": url, "description": description}
        return self.session.post(Paths.PLAN_WEBLINKS.format(test_plan_key),
                                 json=json)

    def create_issue_link(self, test_plan_key: Union[str, int], issue_id: int):
        """
        Creates a link between a test plan and a Jira issue.

        :param test_plan_key: The ID or key of the test plan
        :param issue_id: The issue ID
        :return: dict with response body
        """
        return self.session.post(Paths.PLAN_ISSUES.format(test_plan_key),
                                 json={"issueId": issue_id})

    def create_test_cycle_link(self, test_plan_key: Union[str, int], test_cycle_id: int):
        """
        Creates a link between a test plan and a test cycle.

        :param test_plan_key: The ID or key of the test plan
        :param test_cycle_id: The ID or key of the test cycle
        :return: dict with response body
        """
        return self.session.post(Paths.PLAN_CYCLES.format(test_plan_key),
                                 json={"testCycleIdOrKey": test_cycle_id})

class ScaleIssueLinksEndpoints(IssueLinksEndpoints):
    """
    Api wrapper for "Issue Links" endpoints

    Operations related to coverage of issue links.
    """

    def get_test_plans(self, issue_key: str):
        """
        Get test plan IDs linked to the given Jira issue.

        :param issue_key: The key of the Jira issue
        :return: dict with response body
        """
        return self.session.get(Paths.ISLINKS_PLANS.format(issue_key))
