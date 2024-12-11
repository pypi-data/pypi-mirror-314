from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import httpx

import h2o_mlops_autogen
from h2o_mlops import _core
from h2o_mlops import _environments
from h2o_mlops import _experiments
from h2o_mlops import _models
from h2o_mlops import _projects
from h2o_mlops import _runtimes
from h2o_mlops import _utils
from h2o_mlops import options
from h2o_mlops.errors import MLOpsDeploymentError

DEFAULT_HTTPX_READ_TIMEOUT = 5


class MLOpsScoringDeployment:
    """Interact with a scoring Deployment on H2O MLOps."""

    def __init__(
        self,
        client: _core.Client,
        deployment_id: str,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._deployment_id = deployment_id
        self._environment = environment
        self._experiments: List[_experiments.MLOpsExperiment]
        self._project = project
        self._state_map = {"UNHEALTY": "UNHEALTHY"}
        self._mode: str
        self._init()

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.uid} {self.name}"

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"UID: {self.uid}\n"
            f"Status: {self.status()}\n"
            f"Kubernetes Options:\n{self.kubernetes_options.__str__()}"
        )

    def _init(self) -> None:
        raw_info = self._get_raw_info()
        if raw_info.shadow_deployment:
            self._mode = "Champion/Challenger"
            primary_element = raw_info.shadow_deployment.primary_element
            secondary_element = raw_info.shadow_deployment.secondary_element
            self._experiments = [
                self._project.experiments.get(
                    primary_element.deployment_composition.experiment_id
                ),
                self._project.experiments.get(
                    secondary_element.deployment_composition.experiment_id
                ),
            ]
        if raw_info.single_deployment:
            self._mode = "Single Model"
            self._experiments = [
                self._project.experiments.get(
                    raw_info.single_deployment.deployment_composition.experiment_id
                )
            ]
        if raw_info.split_deployment:
            self._mode = "A/B Test"
            self._experiments = [
                self._project.experiments.get(
                    element.deployment_composition.experiment_id
                )
                for element in raw_info.split_deployment.split_elements
            ]

    @staticmethod
    def _get_deployment_mode(raw_info: Any) -> Optional[str]:
        if raw_info.shadow_deployment:
            return "Champion/Challenger"
        if raw_info.single_deployment:
            return "Single Model"
        if raw_info.split_deployment:
            return "A/B Test"
        return None

    def _get_raw_info(self) -> Any:
        for (
            deployment
        ) in self._client._backend.deployer.deployment.list_project_deployments(
            h2o_mlops_autogen.DeployListProjectDeploymentsRequest(
                project_id=self._project.uid
            )
        ).deployment:
            if deployment.id == self.uid:
                return MLOpsScoringDeployment._patch_deployment(deployment)

    def _get_raw_status(self) -> Any:
        deployer_status = self._client._backend.deployer.deployment_status
        return deployer_status.get_deployment_status(
            h2o_mlops_autogen.DeployGetDeploymentStatusRequest(self.uid)
        ).deployment_status

    @staticmethod
    def _patch_deployment(deployment: Any) -> Any:
        if deployment.single_deployment is not None:
            deployment.single_deployment = (
                MLOpsScoringDeployment._patch_single_deployment(
                    deployment.single_deployment,
                )
            )
        if deployment.security is None:
            deployment.security = h2o_mlops_autogen.DeploySecurity()
        if deployment.monitor is None:
            deployment.monitor = h2o_mlops_autogen.DeployMonitor()

        return deployment

    @staticmethod
    def _patch_single_deployment(single_deployment: Any) -> Any:
        if single_deployment.deployment_environment_variables is None:
            single_deployment.deployment_environment_variables = (
                h2o_mlops_autogen.DeployDeploymentEnvironmentVariables()
            )
        if single_deployment.kubernetes_configuration_shortcut is None:
            single_deployment.kubernetes_configuration_shortcut = (
                h2o_mlops_autogen.DeployKubernetesConfigurationShortcut()
            )
        if single_deployment.kubernetes_resource_spec is None:
            single_deployment.kubernetes_resource_spec = (
                h2o_mlops_autogen.DeployKubernetesResourceSpec()
            )

        kubernetes_resource_spec = single_deployment.kubernetes_resource_spec
        if kubernetes_resource_spec.kubernetes_resource_requirement is None:
            kubernetes_resource_spec.kubernetes_resource_requirement = (
                h2o_mlops_autogen.DeployKubernetesResourceRequirement()
            )
            single_deployment.kubernetes_resource_spec = kubernetes_resource_spec

        return single_deployment

    @property
    def environment(self) -> _environments.MLOpsEnvironment:
        """Deployment environment."""
        return self._environment

    @property
    def environment_variables(self) -> Dict[str, str]:
        """Environment variables added to the scoring runtime."""
        sd = self._get_raw_info().single_deployment
        ev = sd.deployment_environment_variables
        if ev:
            return ev.runtime_variables
        return {}

    @property
    def experiments(self) -> List[_experiments.MLOpsExperiment]:
        """List of experiments in Deployment."""
        return self._experiments

    @property
    def kubernetes_options(self) -> Optional[options.KubernetesOptions]:
        """Deployment Kubernetes resource configuration."""
        if self.mode == "Single Model":
            sd = self._get_raw_info().single_deployment
            krs = sd.kubernetes_resource_spec
            kcs = sd.kubernetes_configuration_shortcut
            return options.KubernetesOptions(
                replicas=krs.replicas,
                requests=krs.kubernetes_resource_requirement.requests,
                limits=krs.kubernetes_resource_requirement.limits,
                affinity=kcs.kubernetes_affinity_shortcut_name,
                toleration=kcs.kubernetes_toleration_shortcut_name,
            )
        return None

    @property
    def mode(self) -> str:
        """Deployment mode (Single Model, A/B Test, Champion Challenger)."""
        return self._mode

    @property
    def monitoring_options(self) -> options.MonitoringOptions:
        """Deployment monitoring configuration."""
        raw_info = self._get_raw_info()
        return options.MonitoringOptions(
            enable=raw_info.monitor.enable,
            save_scoring_inputs=raw_info.monitor.store_scoring_transaction_enable,
        )

    @property
    def name(self) -> str:
        """Deployment display name."""
        return self._get_raw_info().display_name

    @property
    def owner(self) -> str:
        """Deployment owner name."""
        return self._get_raw_info().user_info.owner_name

    @property
    def security_options(self) -> options.SecurityOptions:
        """Deployment security configuration."""
        security_options = options.SecurityOptions()
        token_auth = self._get_raw_info().security.token_auth
        disabled_security = self._get_raw_info().security.disabled_security
        passphrase = self._get_raw_info().security.passphrase
        if passphrase:
            security_options.passphrase = passphrase.hash
            security_options.hashed_passphrase = {
                "PASSPHRASE_HASH_TYPE_UNSPECIFIED": None,
                "PASSPHRASE_HASH_TYPE_PLAINTEXT": False,
                "PASSPHRASE_HASH_TYPE_BCRYPT": True,
                "PASSPHRASE_HASH_TYPE_PBKDF2": True,
            }.get(passphrase.passphrase_hash_type)
        elif (
            token_auth
            and token_auth.authentication_protocol
            == h2o_mlops_autogen.DeployAuthorizationProtocolSecurityType.OIDC
        ):
            security_options.oidc_token_auth = True
        elif (
            disabled_security
            and disabled_security
            == h2o_mlops_autogen.DeployDisabledStateSecurityType.DISABLED
        ):
            security_options.disabled_security = True

        return security_options

    @property
    def uid(self) -> str:
        """Deployment unique ID."""
        return self._deployment_id

    @property
    def url_for_capabilities(self) -> str:
        """Deployment capabilities URL."""
        return self._get_raw_status().scorer.capabilities.url

    @property
    def url_for_sample_request(self) -> str:
        """Deployment sample request URL."""
        return self._get_raw_status().scorer.sample_request.url

    @property
    def url_for_schema(self) -> str:
        """Deployment schema URL."""
        base_url = "/".join(self.url_for_sample_request.split("/")[:-1])
        return f"{base_url}/schema"

    @property
    def url_for_scoring(self) -> str:
        """Deployment scoring URL."""
        return self._get_raw_status().scorer.score.url

    def delete(self) -> None:
        """Delete Deployment."""
        self._client._backend.deployer.deployment.delete_deployment(
            h2o_mlops_autogen.DeployDeleteDeploymentRequest(self.uid)
        )

    def get_capabilities(
        self,
        auth_value: Optional[str] = None,
        timeout: Optional[float] = DEFAULT_HTTPX_READ_TIMEOUT,
    ) -> str:
        """Get capabilities supported by the Deployment, in JSON format.

        Args:
            auth_value: Deployment authorization value
                (passphrase or access token) (if required)
            timeout: Timeout in seconds for the HTTP request
                (optional, default is DEFAULT_HTTPX_READ_TIMEOUT)
        """
        headers = {}
        if auth_value:
            headers["Authorization"] = f"Bearer {auth_value}"
        result = httpx.get(
            self.url_for_capabilities,
            headers=headers,
            timeout=timeout,
            verify=self._client._ssl_context,
        )
        result.raise_for_status()
        return result.json()

    def get_sample_request(
        self,
        auth_value: Optional[str] = None,
        timeout: Optional[float] = DEFAULT_HTTPX_READ_TIMEOUT,
    ) -> str:
        """Get sample request for the Deployment, in JSON format.

        Args:
            auth_value: Deployment authorization value
                (passphrase or access token) (if required)
            timeout: Timeout in seconds for the HTTP request
                (optional, default is DEFAULT_HTTPX_READ_TIMEOUT)
        """
        headers = {}
        if auth_value:
            headers["Authorization"] = f"Bearer {auth_value}"
        result = httpx.get(
            self.url_for_sample_request,
            headers=headers,
            timeout=timeout,
            verify=self._client._ssl_context,
        )
        result.raise_for_status()
        return result.json()

    def get_schema(
        self,
        auth_value: Optional[str] = None,
        timeout: Optional[float] = DEFAULT_HTTPX_READ_TIMEOUT,
    ) -> str:
        """Get schema for the Deployment, in JSON format.

        Args:
            auth_value: Deployment authorization value
                (passphrase or access token) (if required)
            timeout: Timeout in seconds for the HTTP request
                (optional, default is DEFAULT_HTTPX_READ_TIMEOUT)
        """
        headers = {}
        if auth_value:
            headers["Authorization"] = f"Bearer {auth_value}"
        result = httpx.get(
            self.url_for_schema,
            headers=headers,
            timeout=timeout,
            verify=self._client._ssl_context,
        )
        result.raise_for_status()
        return result.json()["schema"]

    def is_healthy(self) -> bool:
        """Check if Deployment status is Healthy."""
        return self.status() == "HEALTHY"

    def raise_for_failure(self) -> None:
        """Raise an error if Deployment status is Failed."""
        if self.status() == "FAILED":
            raise MLOpsDeploymentError("Deployment failed.")

    def set_environment_variables(self, environment_variables: Dict[str, str]) -> None:
        """Set extra environment variables in the scoring runtime.

        Note: this method will remove all previously set extra environment variables.

        Args:
            environment_variables: mapping of variable names to variable values.
        """
        if self.mode == "Single Model":
            environment_variables = (
                h2o_mlops_autogen.DeployDeploymentEnvironmentVariables(
                    runtime_variables=environment_variables,
                )
            )
            raw_info = self._get_raw_info()
            raw_info.single_deployment.deployment_environment_variables = (
                environment_variables
            )
            self._client._backend.deployer.deployment.update_model_deployment(
                h2o_mlops_autogen.DeployUpdateModelDeploymentRequest(
                    deployment=raw_info
                )
            )

    def status(self) -> str:
        """Deployment status."""
        state = self._get_raw_status().state
        return self._state_map.get(state, state)

    def update_kubernetes_options(
        self,
        *,
        replicas: Optional[int] = None,
        requests: Optional[Dict[str, str]] = None,
        limits: Optional[Dict[str, str]] = None,
        affinity: Optional[str] = None,
        toleration: Optional[str] = None,
    ) -> None:
        """Manage hardware resource usage.

        Args:
            replicas: number of deployment replicas to use.
                Set to 0 or -1 to release hardware and completely scale down
                the deployment.
            requests: Kubernetes resource requests as a dictionary.
                For example: {'cpu': '500m', 'memory': '1Gi'}
            limits: Kubernetes resource limits as a dictionary.
                For example: {'memory': '1Gi'}
            affinity: shortcut name for an affinity.
                See `deployment.environment.allowed_affinities`.
            toleration: shortcut name for a toleration.
                See `deployment.environment.allowed_tolerations`.
        """
        if self.mode == "Single Model":
            raw_info = self._get_raw_info()
            krs = raw_info.single_deployment.kubernetes_resource_spec
            kcs = raw_info.single_deployment.kubernetes_configuration_shortcut
            if replicas == 0:
                replicas = -1
            if replicas is not None:
                krs.replicas = replicas
            if requests is not None:
                krs.kubernetes_resource_requirement.requests = requests
            if limits is not None:
                krs.kubernetes_resource_requirement.limits = limits
            if affinity is not None:
                kcs.kubernetes_affinity_shortcut_name = affinity
            if toleration is not None:
                kcs.kubernetes_toleration_shortcut_name = toleration
            raw_info.single_deployment.kubernetes_resource_spec = krs
            raw_info.single_deployment.kubernetes_configuration_shortcut = kcs
            self._client._backend.deployer.deployment.update_model_deployment(
                h2o_mlops_autogen.DeployUpdateModelDeploymentRequest(
                    deployment=raw_info
                )
            )

    def update_monitoring_options(
        self,
        *,
        enable: Optional[bool] = None,
        save_scoring_inputs: Optional[bool] = None,
    ) -> None:
        """Manage model monitoring.

        Args:
            enable: whether monitoring is enabled.
            save_scoring_inputs: whether to store scoring transaction or not.
                If enable is false, this field will be ignored.
        """
        raw_info = self._get_raw_info()
        if enable is not None:
            raw_info.monitor.enable = enable
        if save_scoring_inputs is not None:
            raw_info.monitor.store_scoring_transaction_enable = save_scoring_inputs
        self._client._backend.deployer.deployment.update_model_deployment(
            h2o_mlops_autogen.DeployUpdateModelDeploymentRequest(deployment=raw_info)
        )

    def update_security_options(
        self,
        *,
        passphrase: str,
        hashed_passphrase: Optional[bool] = None,
    ) -> None:
        """Manage passphrase protection.

        Allowed security updates are:
        - no passphrase -> plain text passphrase
        - no passphrase -> hashed passphrase
        - plain text passphrase -> hashed passphrase
        - hashed passphrase -> plain text passphrase
        - old plain text passphrase -> new plain text passphrase
        - old hashed passphrase -> new hashed passphrase

        Args:
            passphrase: passphrase for the endpoint if supplied and not hashed.
            hashed_passphrase: whether the passphrase is hashed.
        """
        raw_info = self._get_raw_info()
        if not passphrase and raw_info.security.passphrase.hash:
            raise RuntimeError("Cannot remove passphrase protection from a deployment.")
        raw_info.security.passphrase.hash = passphrase
        raw_info.security.passphrase.passphrase_hash_type = (
            _utils._detect_passphrase_hash_type(
                security_options=options.SecurityOptions(
                    passphrase=passphrase,
                    hashed_passphrase=hashed_passphrase,
                )
            )
        )
        self._client._backend.deployer.deployment.update_model_deployment(
            h2o_mlops_autogen.DeployUpdateModelDeploymentRequest(deployment=raw_info)
        )


class MLOpsScoringDeployments:
    def __init__(
        self,
        client: _core.Client,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._environment = environment
        self._project = project

    def create_a_b_test(self) -> None:
        raise NotImplementedError

    def create_create_champion_challenger(self) -> None:
        raise NotImplementedError

    def create_single(
        self,
        name: str,
        model: _models.MLOpsModel,
        scoring_runtime: _runtimes.MLOpsScoringRuntime,
        security_options: options.SecurityOptions,
        model_version: Union[int, str] = "latest",
        description: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        kubernetes_options: Optional[options.KubernetesOptions] = None,
        monitoring_options: Optional[options.MonitoringOptions] = None,
    ) -> MLOpsScoringDeployment:
        """Create a single model scoring Deployment in H2O MLOps.

        Args:
            name: Deployment display name
            model: MLOps Registered Model object
            scoring_runtime: MLOps Scoring Runtime object
            security_options: Security Options object
            model_version: MLOps Registered Model version number
            description: Deployment description
            environment_variables: Environment variables to add to the scoring runtime
            kubernetes_options: Kubernetes Options object
            monitoring_options: Monitoring Options object
        """
        experiment = model.get_experiment(model_version=model_version)
        deployable_artifact_type = scoring_runtime._raw_info.deployable_artifact_type
        artifact_processor = scoring_runtime._raw_info.artifact_processor
        composition = h2o_mlops_autogen.DeployDeploymentComposition(
            experiment_id=experiment.uid,
            deployable_artifact_type_name=deployable_artifact_type.name,
            artifact_processor_name=artifact_processor.name,
            runtime_name=scoring_runtime.uid,
        )
        environment_variables = h2o_mlops_autogen.DeployDeploymentEnvironmentVariables(
            runtime_variables=environment_variables,
        )
        if not kubernetes_options:
            kubernetes_options = options.KubernetesOptions()
        kubernetes_resource_requirement = (
            h2o_mlops_autogen.DeployKubernetesResourceRequirement(
                limits=kubernetes_options.limits,
                requests=kubernetes_options.requests,
            )
        )
        kubernetes_resource_spec = h2o_mlops_autogen.DeployKubernetesResourceSpec(
            kubernetes_resource_requirement=kubernetes_resource_requirement,
            replicas=kubernetes_options.replicas,
        )
        self._environment._raise_for_unallowed_affinity(
            affinity=kubernetes_options.affinity
        )
        self._environment._raise_for_unallowed_toleration(
            toleration=kubernetes_options.toleration
        )
        kubernetes_configuration_shortcut = (
            h2o_mlops_autogen.DeployKubernetesConfigurationShortcut(
                kubernetes_affinity_shortcut_name=kubernetes_options.affinity,
                kubernetes_toleration_shortcut_name=kubernetes_options.toleration,
            )
        )
        if not monitoring_options:
            monitoring_options = options.MonitoringOptions()
        if security_options.disabled_security:
            security = h2o_mlops_autogen.DeploySecurity(
                disabled_security=(
                    h2o_mlops_autogen.DeployDisabledStateSecurityType.DISABLED
                ),
            )
        elif security_options.oidc_token_auth:
            security = h2o_mlops_autogen.DeploySecurity(
                token_auth=h2o_mlops_autogen.DeployAuthorizationAccessToken(
                    authentication_protocol=(
                        h2o_mlops_autogen.DeployAuthorizationProtocolSecurityType.OIDC
                    ),
                )
            )
        else:
            security = h2o_mlops_autogen.DeploySecurity(
                passphrase=h2o_mlops_autogen.DeployAuthenticationPassphrase(
                    hash=security_options.passphrase,
                    passphrase_hash_type=_utils._detect_passphrase_hash_type(
                        security_options=security_options
                    ),
                )
            )
        to_deploy = h2o_mlops_autogen.DeployDeployment(
            project_id=self._project.uid,
            deployment_environment_id=self._environment.uid,
            single_deployment=h2o_mlops_autogen.DeploySingleDeployment(
                deployment_composition=composition,
                deployment_environment_variables=environment_variables,
                kubernetes_configuration_shortcut=kubernetes_configuration_shortcut,
                kubernetes_resource_spec=kubernetes_resource_spec,
            ),
            display_name=name,
            description=description,
            monitor=h2o_mlops_autogen.DeployMonitor(
                enable=monitoring_options.enable,
                store_scoring_transaction_enable=monitoring_options.save_scoring_inputs,
            ),
            security=security,
        )
        deployment = self._client._backend.deployer.deployment.create_deployment(
            h2o_mlops_autogen.DeployCreateDeploymentRequest(deployment=to_deploy)
        ).deployment
        return self.get(deployment.id)

    def get(self, uid: str) -> MLOpsScoringDeployment:
        """Get the Deployment object corresponding to a Deployment in H2O MLOps.

        Args:
            uid: H2O MLOps unique ID for the Deployment.
        """
        return MLOpsScoringDeployment(
            self._client, uid, self._environment, self._project
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Deployments available in the Project.

        Examples::

            # filter on columns by using selectors
            environment.deployments.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            deployment = environment.deployments.list()[0]

            # get a new Table using multiple indexes or slices
            table = environment.deployments.list()[2,4]
            table = environment.deployments.list()[2:4]
        """
        srv = self._client._backend.deployer.deployment
        deployments = []
        response = srv.list_project_deployments(
            h2o_mlops_autogen.DeployListProjectDeploymentsRequest(
                project_id=self._project.uid
            )
        )
        deployments += response.deployment
        while response.paging:
            response = srv.list_project_deployments(
                h2o_mlops_autogen.DeployListProjectDeploymentsRequest(
                    project_id=self._project.uid,
                    paging=h2o_mlops_autogen.StoragePagingRequest(
                        page_token=response.paging.next_page_token
                    ),
                )
            )
            deployments += response.deployment
        data = [
            d
            for d in deployments
            if d.deployment_environment_id == self._environment.uid
        ]
        data_as_dicts = [
            {
                "name": d.display_name,
                "mode": MLOpsScoringDeployment._get_deployment_mode(d),
                "uid": d.id,
            }
            for d in data
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "mode", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
