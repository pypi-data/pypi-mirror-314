from kdp_api.models.authentication import Authentication

"""
This class extends Authentication and override the strategy validation to allow
authentication request coming from auth-proxy service.
"""


class ProxyAuthentication(Authentication):

    def __init__(self, first_name: str, workspace_id: str, strategy: str, *args, **kwargs):
        super().__init__(email="", password="", firstName=first_name, workspaceId=workspace_id, strategy=strategy)
