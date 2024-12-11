import os
from typing import Any, Optional
from typing import Callable

from _h2o_mlops_client.deployer import api
from _h2o_mlops_client.deployer import api_client
from _h2o_mlops_client.deployer.exceptions import *  # noqa: F403, F401


class ApiClient(api_client.ApiClient):
    """Overrides update_params_for_auth method of the generated ApiClient classes"""

    def __init__(
        self, configuration: api_client.Configuration, token_provider: Callable[[], str]
    ):
        self._token_provider = token_provider
        super().__init__(configuration=configuration)

    def update_params_for_auth(
        self, headers: Any, querys: Any, auth_settings: Any, request_auth: Any = None
    ) -> None:
        token = self._token_provider()
        headers["Authorization"] = f"Bearer {token}"


class Client:
    """The composite client for accessing Deployer services."""

    def __init__(
        self,
        host: str,
        token_provider: Callable[[], str],
        verify_ssl: bool = True,
        ssl_cacert: Optional[str] = None,
    ):
        configuration = api_client.Configuration(
            host=host,
        )
        configuration.verify_ssl = verify_ssl
        ssl_ca_cert = ssl_cacert or os.getenv("MLOPS_AUTH_CA_FILE_OVERRIDE")
        if ssl_ca_cert:
            configuration.ssl_ca_cert = ssl_ca_cert

        client = ApiClient(
            configuration=configuration,
            token_provider=token_provider,
        )
        self._deployment_status = api.DeploymentStatusServiceApi(api_client=client)
        self._composition = api.CompositionServiceApi(api_client=client)
        self._deployment = api.DeploymentServiceApi(api_client=client)
        self._environment = api.EnvironmentServiceApi(api_client=client)
        self._kubernetes_configuration = api.KubernetesConfigurationServiceApi(
            api_client=client
        )
        self._log = api.LogServiceApi(api_client=client)
        self._endpoint = api.EndpointServiceApi(api_client=client)
        self._profiling = api.DeploymentProfilingServiceApi(api_client=client)

    @property
    def deployment_status(self) -> api.DeploymentStatusServiceApi:
        return self._deployment_status

    @property
    def composition(self) -> api.CompositionServiceApi:
        return self._composition

    @property
    def deployment(self) -> api.DeploymentServiceApi:
        return self._deployment

    @property
    def environment(self) -> api.EnvironmentServiceApi:
        return self._environment

    @property
    def kubernetes_configuration(self) -> api.KubernetesConfigurationServiceApi:
        return self._kubernetes_configuration

    @property
    def log(self) -> api.LogServiceApi:
        return self._log

    @property
    def endpoint(self) -> api.EndpointServiceApi:
        return self._endpoint

    @property
    def profiling(self) -> api.DeploymentProfilingServiceApi:
        return self._profiling
