from __future__ import annotations

import io
import json
from datetime import datetime
from time import sleep
from typing import Any, Dict, Optional, Union

import h2o_mlops_autogen
from h2o_mlops import _core, _experiments, _models
from h2o_mlops import _projects
from h2o_mlops import _utils
from h2o_mlops import options
from h2o_mlops._runtimes import MLOpsScoringRuntime


class MLOpsBatchScoringJob:

    def __init__(
        self,
        client: _core.Client,
        project: _projects.MLOpsProject,
        job: h2o_mlops_autogen.V1Job,
    ):
        self._client = client
        self._job = job
        self._project = project
        self._experiment: Optional[_experiments.MLOpsExperiment] = None
        self._last_seen_output_timestamp = None
        self._runtime: Optional[MLOpsScoringRuntime] = None

    @property
    def uid(self) -> str:
        return self._job.name.split("/")[-1]

    @property
    def name(self) -> str:
        return self._job.display_name

    @property
    def source(self) -> options.BatchSourceOptions:
        source = self._job.source
        return options.BatchSourceOptions(
            spec_uid=source.split("/")[-1],
            config=json.loads(source.config),
            mime_type=options.MimeTypeOptions(source.mime_type),
            location=source.location,
        )

    @property
    def sink(self) -> options.BatchSinkOptions:
        sink = self._job.sink
        return options.BatchSinkOptions(
            spec_uid=sink.split("/")[-1],
            config=json.loads(sink.config),
            mime_type=options.MimeTypeOptions(sink.mime_type),
            location=sink.location,
        )

    @property
    def scoring_runtime(self) -> MLOpsScoringRuntime:
        if self._runtime is None:
            c = self._job.instance_spec.deployment_composition
            self._runtime = self._client.runtimes.scoring.list(uid=c.runtime)[0]

        return self._runtime

    @property
    def experiment(self) -> _experiments.MLOpsExperiment:
        if self._experiment is None:
            self._experiment = self._project.experiments.get(
                self._job.instance_spec.deployment_composition.experiment_id
            )

        return self._experiment

    @property
    def resource_spec(self) -> options.BatchKubernetesOptions:
        resource_spec = self._job.instance_spec.resource_spec
        return options.BatchKubernetesOptions(
            replicas=resource_spec.replicas,
            min_replicas=resource_spec.minimal_available_replicas,
            requests=resource_spec.requests,
            limits=resource_spec.limits,
        )

    @property
    def model_request_parameters(self) -> options.ModelRequestParameters:
        model_request_parameters = self._job.model_request_parameters
        return options.ModelRequestParameters(
            id_field=model_request_parameters.id_field,
            contributions=options.RequestContributionsOptions(
                model_request_parameters.request_contributions
            ),
            prediction_intervals=model_request_parameters.request_prediction_intervals,  # noqa: E501
        )

    @property
    def state(self) -> str:
        return self._job.state.to_str()

    @property
    def creator(self) -> str:
        return self._client._get_username(self._job.creator.split("/")[-1])

    @property
    def create_time(self) -> datetime:
        return self._job.create_time

    @property
    def start_time(self) -> datetime:
        return self._job.start_time

    @property
    def end_time(self) -> datetime:
        return self._job.end_time

    def cancel(self, wait: bool = True) -> None:
        """Cancel this job."""
        srv = self._client._backend.batch.job
        srv.cancel_job(self._job.name)
        if wait:
            self.wait()

    def delete(self) -> None:
        """Delete this job."""
        srv = self._client._backend.batch.job
        srv.delete_job(self._job.name)

    def refresh(self) -> None:
        """Refresh job's state"""
        srv = self._client._backend.batch.job
        response = srv.get_job(self._job.name)
        self._job = response.job

    def logs(self, since_time: Optional[datetime] = None) -> None:
        """Start printing logs since select time."""
        if since_time is None:
            since_time = self._last_seen_output_timestamp

        srv = self._client._backend.batch.job
        response = srv.get_job_output(
            self._job.name, since_time=since_time, _preload_content=False
        )
        try:
            with response:
                for line in io.TextIOWrapper(response):

                    class DataWrapper:
                        def __init__(self, data: Any):
                            self.data = data

                    output = srv.api_client.deserialize(
                        DataWrapper(line), "StreamResultOfV1JobOutputResponse"
                    )
                    if output.error:
                        print(f"Error: {output.error}")
                    else:
                        result = output.result
                        if result.error:
                            print(f"Error: {result.error}")
                        else:
                            print(
                                f"[{result.pod_name}.{result.container_name}] "
                                f"{result.line}"
                            )

                    if (
                        output.result is not None
                        and output.result.timestamp is not None
                    ):
                        self._last_seen_output_timestamp = output.result.timestamp
        finally:
            response.release_conn()

    def wait(self, logs: bool = True) -> None:
        """Wait for job to complete.
        If logs is set to True, the job's logs will be printed out."""
        while self._job.end_time is None:
            if logs:
                self.logs()
            else:
                sleep(5)
            self.refresh()


class MLOpsBatchScoringJobs:
    """
    Class for managing batch scoring jobs.
    """

    def __init__(self, client: _core.Client, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def create(
        self,
        *,
        source: options.BatchSourceOptions,
        sink: options.BatchSinkOptions,
        model: _models.MLOpsModel,
        model_version: Union[int, str] = "latest",
        scoring_runtime: MLOpsScoringRuntime,
        environment_variables: Optional[Dict[str, str]] = None,
        resource_spec: Optional[options.BatchKubernetesOptions] = None,
        concurrency: Optional[int] = None,
        mini_batch_size: Optional[int] = None,
        model_request_parameters: Optional[options.ModelRequestParameters] = None,
        name: Optional[str] = None,
    ) -> MLOpsBatchScoringJob:
        """Create a new batch scoring job."""
        experiment = model.get_experiment(model_version=model_version)
        deployable_artifact_type = scoring_runtime._raw_info.deployable_artifact_type
        artifact_processor = scoring_runtime._raw_info.artifact_processor

        composition = h2o_mlops_autogen.V1DeploymentComposition(
            artifact_processor=artifact_processor.name,
            experiment_id=experiment.uid,
            artifact_type=deployable_artifact_type.name,
            runtime=scoring_runtime.uid,
        )

        api_resource_spec = None
        if resource_spec is not None:
            kubernetes_resource_requirement = h2o_mlops_autogen.V1ResourceRequirement(
                limits=resource_spec.limits,
                requests=resource_spec.requests,
            )

            api_resource_spec = h2o_mlops_autogen.V1ResourceSpec(
                resource_requirement=kubernetes_resource_requirement,
                replicas=resource_spec.replicas,
                minimal_available_replicas=resource_spec.min_replicas,
            )

        instance_spec = h2o_mlops_autogen.V1InstanceSpec(
            deployment_composition=composition,
            resource_spec=api_resource_spec,
            environment_variables=environment_variables,
        )

        batch_parameters = h2o_mlops_autogen.V1BatchParameters(
            concurrency=concurrency,
            mini_batch_size=mini_batch_size,
        )

        api_model_request_parameters = None
        if model_request_parameters is not None:
            api_model_request_parameters = h2o_mlops_autogen.V1ModelRequestParameters(
                id_field=model_request_parameters.id_field,
                request_contributions=(
                    model_request_parameters.contributions.value
                    if model_request_parameters.contributions
                    else None
                ),
                request_prediction_intervals=model_request_parameters.prediction_intervals,  # noqa: E501
            )

        api_source = h2o_mlops_autogen.V1Source(
            spec=f"sourceSpecs/{source.spec_uid}",
            config=json.dumps(source.config),
            mime_type=source.mime_type.value,
            location=source.location,
        )

        api_sink = h2o_mlops_autogen.V1Sink(
            spec=f"sinkSpecs/{sink.spec_uid}",
            config=json.dumps(sink.config),
            mime_type=sink.mime_type.value,
            location=sink.location,
        )

        job = h2o_mlops_autogen.V1Job(
            display_name=name,
            source=api_source,
            sink=api_sink,
            instance_spec=instance_spec,
            batch_parameters=batch_parameters,
            model_request_parameters=api_model_request_parameters,
        )

        srv = self._client._backend.batch.job
        result = srv.create_job(f"workspaces/{self._project.uid}", job)
        return MLOpsBatchScoringJob(self._client, self._project, result.job)

    def get(self, uid: str) -> MLOpsBatchScoringJob:
        """Get a batch scoring job by ID."""
        srv = self._client._backend.batch.job
        response = srv.get_job(f"workspaces/{self._project.uid}/jobs/{uid}")

        return MLOpsBatchScoringJob(self._client, self._project, response.job)

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Batch Scoring Jobs available in the Project.

        Examples::

            # filter on columns by using selectors
            projects.jobs.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            job = projects.jobs.list()[0]

            # get a new Table using multiple indexes or slices
            table = projects.jobs.list()[2,4]
            table = projects.jobs.list()[2:4]
        """
        srv = self._client._backend.batch.job
        jobs = []
        response = srv.list_jobs(parent=f"workspaces/{self._project.uid}")

        jobs += response.jobs
        while response.next_page_token:
            response = srv.list_jobs(
                parent=f"workspaces/{self._project.uid}",
                page_token=response.next_page_token,
            )
            jobs += response.jobs

        data_as_dicts = [
            {
                "name": job.display_name,
                "uid": job.name.split("/")[-1],
                "job": job,
            }
            for job in jobs
        ]

        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "uid"],
            get_method=lambda x: MLOpsBatchScoringJob(
                self._client, self._project, x["job"]
            ),
            **selectors,
        )
