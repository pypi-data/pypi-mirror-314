"""
A module with the Zephyr Squad base object.
"""

import logging

from zephyr.common.cloud.zephyr_cloud_session import ZephyrScaleSession
from zephyr.squad.zephyr_squad_session import ZephyrSquadSession
from zephyr.squad.cloud.cloud_api import CloudApiWrapper
from zephyr.squad.server.server_api import ServerApiWrapper
from zephyr.squad.server.actions import ServerActionsWrapper

DEFAULT_BASE_URL = "https://prod-api.zephyr4jiracloud.com/v2/"

API_V2 = "v2"
API_V1 = "v1"

class ZephyrSquad:
    """
    Zephyr Squad base object to interact with other objects or raw api
    by its methods. You should define the API version of Zephyr Squad instance
    you are going to work with. Server is v1 and Cloud is v2.

    :param base_url: base API url to connect with. An example for
                     Squad Server looks like 'https://jira.hosted.com'
    :param api_version: 'v2' for Cloud and 'v1' for Server

    :raises ValueError: if api_version is not 'v1' or 'v2'
    """
    def __init__(self, base_url=None, api_version=API_V2, **kwargs):
        base_url = DEFAULT_BASE_URL if not base_url else base_url

        if api_version.lower() == API_V2:
            # The API for Scale and Squad Cloud is almost identical
            session = ZephyrScaleSession(base_url=base_url, **kwargs)
            self.api = CloudApiWrapper(session)
        elif api_version.lower() == API_V1:
            session = ZephyrSquadSession(base_url=base_url, **kwargs)
            self.api = ServerApiWrapper(session)
            self.actions = ServerActionsWrapper(session)
        else:
            raise ValueError("API version should be either 'v1' (Server) or 'v2' (Cloud)")
        self.logger = logging.getLogger(__name__)

    @classmethod
    def server_api(cls, base_url, **kwargs):
        """Alternative constructor for Zephyr Squad Server client"""
        return cls(base_url=base_url, api_version=API_V1, **kwargs)
