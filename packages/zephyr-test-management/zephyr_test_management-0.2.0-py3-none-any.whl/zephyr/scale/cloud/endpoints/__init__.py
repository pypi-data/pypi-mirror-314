from zephyr.common.cloud.endpoints.endpoints import(
    TestCycleEndpoints,
    TestExecutionEndpoints,
    FolderEndpoints,
    StatusEndpoints,
    PriorityEndpoints,
    EnvironmentEndpoints,
    ProjectEndpoints,
    LinkEndpoints,
    AutomationEndpoints,
    HealthcheckEndpoints
)

from .endpoints import (
    ScaleTestCaseEndpoints as TestCaseEndpoints,
    TestPlanEndpoints,
    ScaleIssueLinksEndpoints as IssueLinksEndpoints
)
