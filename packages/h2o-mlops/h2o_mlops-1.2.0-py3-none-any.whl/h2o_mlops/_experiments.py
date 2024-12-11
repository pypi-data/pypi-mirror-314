from __future__ import annotations

import io
import json
import mimetypes
import pathlib
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import h2o_mlops_autogen
from h2o_mlops import _core
from h2o_mlops import _projects
from h2o_mlops import _utils


class MLOpsExperimentArtifact:
    def __init__(self, client: _core.Client, raw_info: Any):
        self._client = client
        self._raw_info = raw_info

    @property
    def name(self) -> str:
        """Artifact display name."""
        return self._raw_info.type

    @property
    def mime_type(self) -> str:
        """Artifact MIME type."""
        return self._raw_info.mime_type

    @property
    def uid(self) -> str:
        """Artifact unique ID."""
        return self._raw_info.id

    def download(
        self,
        directory: Optional[str] = None,
        file_name: Optional[str] = None,
        overwrite: bool = False,
    ) -> str:
        """Download an Artifact.

        Args:
            directory: path to the directory where the file should be saved.
                By default, the current working directory is used.
            file_name: set the name of the file the artifact is saved to.
                By default, the artifact name is used.
            overwrite: overwrite existing files.
        """
        if directory:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        else:
            directory = "./"
        if not file_name:
            file_name = self.name
        dst_path = str(pathlib.Path(directory, file_name))

        try:
            if overwrite:
                mode = "wb"
            else:
                mode = "xb"
            with open(dst_path, mode) as f:
                self._client._backend.storage.artifact.download_artifact(
                    artifact_id=self.uid, file=f
                )
        except FileExistsError:
            print(f"{dst_path} already exists. Use `overwrite` to force download.")
            raise

        return dst_path

    def to_dictionary(self) -> Dict[str, Any]:
        """Convert the Artifact to a Python dictionary, if possible."""
        if self.mime_type not in ["application/json"]:
            raise RuntimeError(
                f"Artifact with mime_type '{self.mime_type}' "
                "cannot be converted to a dictionary."
            )
        with io.BytesIO() as f:
            self._client._backend.storage.artifact.download_artifact(
                artifact_id=self.uid, file=f
            )
            return json.loads(f.getvalue().decode())

    def to_string(self) -> str:
        """Convert the Artifact to a Python string, if possible."""
        if self.mime_type not in ["application/json", "text/plain"]:
            raise RuntimeError(
                f"Artifact with mime_type '{self.mime_type}' "
                "cannot be converted to a string."
            )
        with io.BytesIO() as f:
            self._client._backend.storage.artifact.download_artifact(
                artifact_id=self.uid, file=f
            )
            return f.getvalue().decode()


class MLOpsExperimentArtifacts:
    def __init__(self, client: _core.Client, experiment: MLOpsExperiment):
        self._client = client
        self._experiment = experiment

    def add(
        self, data: str, mime_type: Optional[str] = None
    ) -> MLOpsExperimentArtifact:
        """Add a new artifact to an Experiment.

        Args:
            data: relative path to the artifact being uploaded
            mime_type: specify the data's media type in the MIME type format.
                If not specified, auto-detection of the media type will be attempted.
        """
        if not mime_type:
            try:
                mime_type = mimetypes.types_map[pathlib.Path(data).suffix]
            except KeyError:
                raise RuntimeError("File MIME type not recognized.")
        artifact = self._client._backend.storage.artifact.create_artifact(
            h2o_mlops_autogen.StorageCreateArtifactRequest(
                artifact=h2o_mlops_autogen.StorageArtifact(
                    entity_id=self._experiment.uid,
                    mime_type=mime_type,
                    type=pathlib.Path(data).name,
                )
            )
        ).artifact
        with open(data, mode="rb") as f:
            self._client._backend.storage.artifact.upload_artifact(
                file=f, artifact_id=artifact.id
            )
        return self.get(uid=artifact.id)

    def get(self, uid: str) -> MLOpsExperimentArtifact:
        """Get the Artifact object corresponding to an H2O MLOps Artifact.

        Args:
            uid: H2O MLOps unique ID for the Artifact.
        """
        raw_info = self._client._backend.storage.artifact.get_artifact(
            h2o_mlops_autogen.StorageGetArtifactRequest(id=uid)
        ).artifact
        return MLOpsExperimentArtifact(client=self._client, raw_info=raw_info)

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """List all Artifacts for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.artifacts.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            artifact = experiment.artifacts.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.artifacts.list()[2,4]
            table = experiment.artifacts.list()[2:4]
        """
        srv = self._client._backend.storage.artifact
        artifacts = srv.list_entity_artifacts(
            h2o_mlops_autogen.StorageListEntityArtifactsRequest(
                entity_id=self._experiment.uid
            )
        ).artifact
        data_as_dicts = [
            {
                "name": a.type,
                "mime_type": a.mime_type[:25],
                "uid": a.id,
            }
            for a in artifacts
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "mime_type", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )


class MLOpsExperimentComments:
    def __init__(self, client: _core.Client, experiment: MLOpsExperiment):
        self._client = client
        self._experiment = experiment

    def add(self, message: str) -> None:
        """Add a new Comment to the Experiment.

        Args:
            message: text displayed by the Comment.
        """
        self._client._backend.storage.experiment.create_experiment_comment(
            h2o_mlops_autogen.StorageCreateExperimentCommentRequest(
                experiment_id=self._experiment.uid, comment_message=message
            )
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """List Comments for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.comments.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            comment = experiment.comments.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.comments.list()[2,4]
            table = experiment.comments.list()[2:4]
        """
        comments = []
        response = self._client._backend.storage.experiment.list_experiment_comments(
            h2o_mlops_autogen.StorageListExperimentCommentsRequest(
                experiment_id=self._experiment.uid,
            )
        )
        comments += response.comment
        while response.paging:
            response = (
                self._client._backend.storage.experiment.list_experiment_comments(
                    h2o_mlops_autogen.StorageListExperimentCommentsRequest(
                        experiment_id=self._experiment.uid,
                        paging=h2o_mlops_autogen.StoragePagingRequest(
                            page_token=response.paging.next_page_token
                        ),
                    )
                )
            )
            comments += response.comment
        data = [
            dict(
                created=comment.created_time.strftime("%Y-%m-%d %I:%M:%S %p"),
                author=self._client._get_username(comment.author_id),
                message=comment.message,
            )
            for comment in comments
        ]
        data = sorted(data, key=lambda x: x["created"])
        return _utils.Table(
            data=data,
            keys=["created", "author", "message"],
            get_method=lambda x: x,
            **selectors,
        )


class MLOpsExperimentTags:
    def __init__(
        self,
        client: _core.Client,
        experiment: MLOpsExperiment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._experiment = experiment
        self._project = project

    def add(self, label: str) -> None:
        """Add a Tag to the Experiment.

        Args:
            label: text displayed by the Tag.
        """
        tag = self._experiment._project.tags.get_or_create(label)
        self._client._backend.storage.experiment.tag_experiment(
            h2o_mlops_autogen.StorageTagExperimentRequest(
                experiment_id=self._experiment.uid, tag_id=tag.uid
            )
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """List Tags for the Experiment.

        Examples::

            # filter on columns by using selectors
            experiment.tags.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            tag = experiment.tags.list()[0]

            # get a new Table using multiple indexes or slices
            table = experiment.tags.list()[2,4]
            table = experiment.tags.list()[2:4]
        """
        # refresh list of tags
        tags = self._experiment._project.experiments.get(
            self._experiment.uid
        )._raw_info.tag
        data = [
            {"label": t.display_name, "uid": t.id}
            for t in tags
            if t.project_id == self._project.uid
        ]
        return _utils.Table(
            data=data,
            keys=["label"],
            get_method=lambda x: _projects.MLOpsProjectTag(
                self._client, self._project, x
            ),
            **selectors,
        )

    def remove(self, label: str) -> None:
        """Remove a Tag from the Experiment.

        Args:
            label: text displayed by the Tag.
        """
        tags = self._experiment.tags.list(label=label)
        if not tags:
            return
        tag = tags[0]
        self._client._backend.storage.experiment.untag_experiment(
            h2o_mlops_autogen.StorageUntagExperimentRequest(
                experiment_id=self._experiment.uid, tag_id=tag.uid
            )
        )


class MLOpsExperiment:
    """Interact with an Experiment on H2O MLOps."""

    def __init__(
        self, client: _core.Client, project: _projects.MLOpsProject, raw_info: Any
    ):
        self._artifacts: Optional[List[Any]] = None
        self._client = client
        self._project = project
        self._raw_info = raw_info

    @property
    def artifacts(self) -> MLOpsExperimentArtifacts:
        """Interact with artifacts for the Experiment."""
        return MLOpsExperimentArtifacts(self._client, self)

    @property
    def comments(self) -> MLOpsExperimentComments:
        """Interact with comments for the Experiment."""
        return MLOpsExperimentComments(self._client, self)

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._raw_info.metadata.values

    @property
    def name(self) -> str:
        """Experiment display name."""
        return self._raw_info.display_name

    @property
    def owner(self) -> str:
        """Experiment owner name."""
        return self._client._get_username(self._raw_info.owner_id)

    @property
    def scoring_artifact_types(self) -> List[str]:
        """List artifact types available for scoring."""
        if not self._artifacts:
            srv = self._client._backend.storage.artifact
            self._artifacts = srv.list_entity_artifacts(
                h2o_mlops_autogen.StorageArtifact(entity_id=self.uid)
            ).artifact

        artifact_name_mapping = {
            "python/mlflow": "python/mlflow.zip",
            "dai/mojo_pipeline": "dai_mojo_pipeline",
            "dai/scoring_pipeline": "dai_python_scoring_pipeline",
            "h2o3/mojo": "h2o3_mojo",
            "python/pickle": "python/pickle",
            "mlflow/mojo_pipeline": "mlflow_mojo_pipeline",
            "mlflow/scoring_pipeline": "mlflow_scoring_pipeline",
            "mlflow/h2o3_mojo": "mlflow_h2o3_mojo",
            "vllm/config": "vllm_config",
        }

        return [
            artifact_name_mapping[a.type]
            for a in self._artifacts
            if a.type in artifact_name_mapping
        ]

    @property
    def tags(self) -> MLOpsExperimentTags:
        """Interact with Tags for the Experiment."""
        return MLOpsExperimentTags(self._client, self, self._project)

    @property
    def uid(self) -> str:
        """Experiment unique ID."""
        return self._raw_info.id

    def delete(self) -> None:
        """Delete Experiment from the Project in H2O MLOps."""
        self._client._backend.storage.experiment.delete_experiment(
            h2o_mlops_autogen.StorageDeleteExperimentRequest(
                id=self.uid, project_id=self._project.uid
            )
        )


class MLOpsExperiments:
    def __init__(self, client: _core.Client, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def create(self, data: str, name: str) -> MLOpsExperiment:
        """Create an Experiment in H2O MLOps.

        Args:
            data: relative path to the experiment artifact being uploaded
            name: display name for Experiment
        """
        artifact = self._client._backend.storage.artifact.create_artifact(
            h2o_mlops_autogen.StorageCreateArtifactRequest(
                h2o_mlops_autogen.StorageArtifact(
                    entity_id=self._project.uid, mime_type=mimetypes.types_map[".zip"]
                )
            )
        ).artifact

        with open(data, mode="rb") as z:
            self._client._backend.storage.artifact.upload_artifact(
                file=z, artifact_id=artifact.id
            )

        ingestion = self._client._backend.ingest.model.create_model_ingestion(
            h2o_mlops_autogen.IngestModelIngestion(artifact_id=artifact.id)
        ).ingestion
        model_metadata = _utils._convert_metadata(ingestion.model_metadata)
        model_params = h2o_mlops_autogen.StorageExperimentParameters()
        if ingestion.model_parameters is not None:
            model_params.target_column = ingestion.model_parameters.target_column

        experiment = self._client._backend.storage.experiment.create_experiment(
            h2o_mlops_autogen.StorageCreateExperimentRequest(
                project_id=self._project.uid,
                experiment=h2o_mlops_autogen.StorageExperiment(
                    display_name=name,
                    metadata=model_metadata,
                    parameters=model_params,
                ),
            )
        ).experiment

        artifact.entity_id = experiment.id
        artifact.type = ingestion.artifact_type

        self._client._backend.storage.artifact.update_artifact(
            h2o_mlops_autogen.StorageUpdateArtifactRequest(
                artifact=artifact, update_mask="type,entityId"
            )
        )

        return self.get(experiment.id)

    def get(self, uid: str) -> MLOpsExperiment:
        """Get the Experiment object corresponding to an H2O MLOps Experiment.

        Args:
            uid: H2O MLOps unique ID for the Experiment.
        """
        experiment = self._client._backend.storage.experiment.get_experiment(
            h2o_mlops_autogen.StorageGetExperimentRequest(
                id=uid,
                response_metadata=h2o_mlops_autogen.StorageKeySelection(
                    pattern=[
                        "source",
                        "score",
                        "dai/score",
                        "scorer",
                        "dai/scorer",
                        "test_score",
                        "dai/test_score",
                        "validation_score",
                        "dai/validation_score",
                        "tool_version",
                        "dai/tool_version",
                        "model_parameters",
                        "dai/model_parameters",
                        "model_type",
                        "tool",
                        "mlflow/flavors/python_function/loader_module",
                    ]
                ),
            )
        ).experiment
        return MLOpsExperiment(self._client, self._project, experiment)

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Experiments available in the Project.

        Examples::

            # filter on columns by using selectors
            project.experiments.list(name="experiment-demo")

            # use an index to get an H2O MLOps entity referenced by the table
            experiment = project.experiments.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.experiments.list()[2,4]
            table = project.experiments.list()[2:4]
        """
        # construct tag filter if possible and asked for
        tag_filter = None
        tag_label = selectors.pop("tag", None)
        if tag_label and self._project.tags.list(label=tag_label):
            tag = self._project.tags.get_or_create(tag_label)
            tag_filter = h2o_mlops_autogen.StorageFilterRequest(
                query=h2o_mlops_autogen.StorageQuery(
                    clause=[
                        h2o_mlops_autogen.StorageClause(
                            tag_constraint=[
                                h2o_mlops_autogen.StorageTagConstraint(tag_id=tag.uid)
                            ]
                        )
                    ]
                )
            )
        # no need to search experiments if tag asked for does not exist in project
        if tag_filter is None and tag_label:
            data = []
        else:
            experiments = []
            response = self._client._backend.storage.experiment.list_experiments(
                h2o_mlops_autogen.StorageListExperimentsRequest(
                    project_id=self._project.uid, filter=tag_filter
                )
            )
            experiments += response.experiment
            while response.paging:
                response = self._client._backend.storage.experiment.list_experiments(
                    h2o_mlops_autogen.StorageListExperimentsRequest(
                        project_id=self._project.uid,
                        paging=h2o_mlops_autogen.StoragePagingRequest(
                            page_token=response.paging.next_page_token
                        ),
                        filter=tag_filter,
                    )
                )
                experiments += response.experiment
            data = [
                {
                    "name": m.display_name,
                    "uid": m.id,
                    "tags": "\n".join(
                        [
                            t.display_name
                            for t in m.tag
                            if t.project_id == self._project.uid
                        ]
                    ),
                }
                for m in experiments
            ]
        return _utils.Table(
            data=data,
            keys=["name", "uid", "tags"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
