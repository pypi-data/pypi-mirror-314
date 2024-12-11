from __future__ import annotations

from typing import Optional

import h2o_mlops_autogen
from h2o_mlops import _core
from h2o_mlops import _deployments
from h2o_mlops import _environments
from h2o_mlops import _projects
from h2o_mlops import _utils


class MLOpsEndpoint:
    """Interact with an Endpoint on H2O MLOps."""

    def __init__(
        self,
        client: _core.Client,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
        uid: str,
    ):
        self._client = client
        self._environment = environment
        self._project = project
        self._parent_resource_name = (
            f"projects/{project.uid}/environments/{environment.uid}"
        )
        self._resource_name = f"{self._parent_resource_name}/endpoints/{uid}"
        self._uid = uid
        self._update()

    def _update(self) -> None:
        self._raw_info = self._client._backend.deployer.endpoint.get_endpoint(
            h2o_mlops_autogen.DeployGetEndpointRequest(name=self._resource_name)
        ).endpoint

    @property
    def description(self) -> str:
        """Endpoint description."""
        self._update()
        return self._raw_info.description

    @property
    def name(self) -> str:
        """Endpoint display name."""
        self._update()
        return self._raw_info.display_name

    @property
    def path(self) -> str:
        """Path the Endpoint appends to the MLOps URL."""
        return self._raw_info.path

    @property
    def target_deployment(
        self,
    ) -> Optional[_deployments.MLOpsScoringDeployment]:
        """MLOps deployment the Endpoint points to."""
        self._update()
        if self._raw_info.target:
            target_uid = self._raw_info.target.split("/")[-1]
            return self._environment.deployments.get(target_uid)
        return None

    @property
    def uid(self) -> str:
        """Endpoint unique ID."""
        return self._uid

    def delete(self) -> None:
        """Delete the Endpoint."""
        self._client._backend.deployer.endpoint.delete_endpoint(
            h2o_mlops_autogen.DeployDeleteEndpointRequest(name=self._resource_name)
        )

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        target_deployment: Optional[_deployments.MLOpsScoringDeployment] = None,
    ) -> None:
        """Change Endpoint settings.

        Args:
           name: display name for the Endpoint
           description: description for the Endpoint
           target_deployment: MLOps deployment the Endpoint points to.
               Set to empty string to disable the Endpoint.
        """
        self._update()
        raw_info = self._raw_info
        if name:
            raw_info.display_name = name
        if description:
            raw_info.description = description
        if target_deployment:
            deployment_resource_name = (
                f"{self._parent_resource_name}/deployments/{target_deployment.uid}"
            )
            raw_info.target = deployment_resource_name
        self._client._backend.deployer.endpoint.update_endpoint(
            h2o_mlops_autogen.DeployUpdateEndpointRequest(endpoint=raw_info)
        )


class MLOpsEndpoints:
    def __init__(
        self,
        client: _core.Client,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._environment = environment
        self._project = project
        self._parent_resource_name = (
            f"projects/{project.uid}/environments/{environment.uid}"
        )

    def create(
        self,
        name: str,
        path: str,
        description: Optional[str] = None,
        target_deployment: Optional[_deployments.MLOpsScoringDeployment] = None,
    ) -> MLOpsEndpoint:
        """Create an Endpoint in H2O MLOps.

        Args:
           name: display name for the Endpoint
           path: path to use for the target deployment URLs
           description: description for the Endpoint
           target_deployment: MLOps deployment the Endpoint points to
        """
        deployment_resource_name = ""
        if target_deployment:
            deployment_resource_name = (
                f"{self._parent_resource_name}/deployments/{target_deployment.uid}"
            )
        endpoint_definition = h2o_mlops_autogen.DeployConfigurableEndpoint(
            display_name=name,
            description=description or "",
            path=path,
            target=deployment_resource_name,
        )
        raw_info = self._client._backend.deployer.endpoint.create_endpoint(
            h2o_mlops_autogen.DeployCreateEndpointRequest(
                parent=self._parent_resource_name, endpoint=endpoint_definition
            )
        ).endpoint
        uid = raw_info.name.split("/")[-1]
        return MLOpsEndpoint(
            client=self._client,
            environment=self._environment,
            project=self._project,
            uid=uid,
        )

    def get(self, uid: str) -> MLOpsEndpoint:
        """Get the Endpoint object corresponding to an H2O MLOps Endpoint.

        Args:
            uid: H2O MLOps unique ID for the Endpoint.
        """
        return MLOpsEndpoint(
            client=self._client,
            environment=self._environment,
            project=self._project,
            uid=uid,
        )

    def list(self, **selectors: Optional[str]) -> _utils.Table:  # noqa A003
        """Retrieve Table of Endpoint available in the Environment.

        Examples::

            # filter on columns by using selectors
            environment.endpoints.list(name="endpoint-demo")


            # use an index to get an H2O MLOps entity referenced by the table
            endpoint = environment.endpoints.list()[0]

            # get a new Table using multiple indexes or slices
            table = environment.endpoints.list()[2,4]
            table = environment.endpoints.list()[2:4]
        """
        endpoints = []
        response = self._client._backend.deployer.endpoint.list_endpoints(
            h2o_mlops_autogen.DeployListEndpointsRequest(
                parent=self._parent_resource_name
            )
        )
        endpoints += response.endpoints
        while response.next_page_token:
            response = self._client._backend.deployer.endpoint.list_endpoints(
                h2o_mlops_autogen.DeployListEndpointsRequest(
                    parent=self._parent_resource_name,
                    page_token=response.next_page_token,
                )
            )
            endpoints += response.endpoints
        data = [
            {"name": e.display_name, "path": e.path, "uid": e.name.split("/")[-1]}
            for e in endpoints
        ]
        return _utils.Table(
            data=data,
            keys=["name", "path", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
