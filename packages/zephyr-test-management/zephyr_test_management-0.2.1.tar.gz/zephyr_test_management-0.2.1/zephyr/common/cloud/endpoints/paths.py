"""Paths to form Cloud API URLs"""


class CloudPaths:
    """
    Common Zephyr Scale and Squad Cloud API paths based on:
    https://support.smartbear.com/zephyr-scale-cloud/api-docs/
    https://smartbear.portal.swaggerhub.com/zephyr-squad/
    """
    # Test Cases
    CASES = "testcases"
    CASE_KEY = "testcases/{}"
    CASE_LINKS = "testcases/{}/links"
    CASE_ISSUES = "testcases/{}/links/issues"
    CASE_WEBLINKS = "testcases/{}/links/weblinks"
    CASE_SCRIPT = "testcases/{}/testscript"
    CASE_STEPS = "testcases/{}/teststeps"

    # Test Cycles
    CYCLES = "testcycles"
    CYCLE_KEY = "testcycles/{}"
    CYCLE_LINKS = "testcycles/{}/links"
    CYCLE_ISSUES = "testcycles/{}/links/issues"
    CYCLE_WEBLINKS = "testcycles/{}/links/weblinks"

    # Test Executions
    EXECUTIONS = "testexecutions"
    EXECUTIONS_KEY = "testexecutions/{}"
    EXECUTIONS_LINKS = "testexecutions/{}/links"
    EXECUTIONS_ISSUES = "testexecutions/{}/links/issues"
    EXECUTIONS_STEPS = "testexecutions/{}/teststeps"

    # Folders
    FOLDERS = "folders"
    FOLDER_KEY = "folders/{}"

    # Statuses
    STATUSES = "statuses"
    STATUSES_ID = "statuses/{}"

    # Priorities
    PRIORITIES = "priorities"
    PRIORITIES_ID = "priorities/{}"

    # Environments
    ENVIRONMENTS = "environments"
    ENVIRONMENTS_ID = "environments/{}"

    # Projects
    PROJECTS = "projects"
    PROJECTS_KEY = "projects/{}"

    # Links
    LINKS_ID = "links/{}"

    # Issue Links
    ISLINKS_CASES = "issuelinks/{}/testcases"
    ISLINKS_CYCLES = "issuelinks/{}/testcycles"
    ISLINKS_EXECS = "issuelinks/{}/executions"

    # Automations
    AUT_CUSTOM = "automations/executions/custom"
    AUT_CUCUMBER = "automations/executions/cucumber"
    AUT_JUNIT = "automations/executions/junit"
    AUT_CASES = "automations/testcases"

    # Healthcheck
    HEALTHCHECK = "healthcheck"
