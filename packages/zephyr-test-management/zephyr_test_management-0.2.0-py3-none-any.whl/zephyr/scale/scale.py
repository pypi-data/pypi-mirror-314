"""
A module with the Zephyr Scale base object.
"""

import logging

from zephyr.common.cloud.zephyr_cloud_session import ZephyrScaleSession
from zephyr.scale.cloud.cloud_api import CloudApiWrapper
from zephyr.scale.server.server_api import ServerApiWrapper


DEFAULT_BASE_URL = "https://api.zephyrscale.smartbear.com/v2/"

API_V2 = "v2"
API_V1 = "v1"


class ZephyrScale:
    """
    Zephyr Scale base object to interact with raw Zephyr APIs or other Zephyr entities. You should
    define the API version of Zephyr Scale instance you are going to work with. Server is v1 and
    Cloud is v2.

    NOTE: Cloud API accepts only token auth, whereas Server API works with Jira auth methods.

    :param base_url: base API url to connect with
    :param api_version: 'v2' for Cloud and 'v1' for Server

    :raises ValueError: if api_version is not 'v1' or 'v2'
    """
    def __init__(self, base_url=None, api_version=API_V2, **kwargs):
        base_url = DEFAULT_BASE_URL if not base_url else base_url
        session = ZephyrScaleSession(base_url=base_url, **kwargs)

        if api_version.lower() == API_V2:
            self.api = CloudApiWrapper(session)
        elif api_version.lower() == API_V1:
            self.api = ServerApiWrapper(session)
        else:
            raise ValueError("API version should be either 'v1' (Server) or 'v2' (Cloud)")
        self.logger = logging.getLogger(__name__)

    @classmethod
    def server_api(cls, base_url, **kwargs):
        """
        Alternative constructor for Zephyr Scale Server client.

        :param base_url: base API url to connect with
        """
        return cls(base_url=base_url, api_version=API_V1, **kwargs)
