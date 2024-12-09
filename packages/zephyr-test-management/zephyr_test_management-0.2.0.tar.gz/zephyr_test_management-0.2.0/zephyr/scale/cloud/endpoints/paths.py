"""Paths to form Cloud API URLs"""

from zephyr.common.cloud.endpoints.paths import CloudPaths

class ScaleCloudPaths(CloudPaths):
    """
    Zephyr Scale Cloud API paths based on:
    https://support.smartbear.com/zephyr-scale-cloud/api-docs/
    """
    # Test Cases
    CASE_VERS = "testcases/{}/versions"
    CASE_VER = "testcases/{}/versions/{}"

    # Test Plans
    PLANS = "testplans"
    PLAN_KEY = "testplans/{}"
    PLAN_WEBLINKS = "testplans/{}/links/weblinks"
    PLAN_ISSUES = "testplans/{}/links/issues"
    PLAN_CYCLES = "testplans/{}/links/testcycles"

    # Issue Links
    ISLINKS_PLANS = "issuelinks/{}/testplans"
