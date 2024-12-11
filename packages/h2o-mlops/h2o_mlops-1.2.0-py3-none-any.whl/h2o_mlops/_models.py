from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Union

import h2o_mlops_autogen
from h2o_mlops import _core
from h2o_mlops import _experiments
from h2o_mlops import _projects
from h2o_mlops import _utils


class MLOpsModel:
    """Interact with a Registered Model on H2O MLOps."""

    def __init__(
        self, client: _core.Client, project: _projects.MLOpsProject, raw_info: Any
    ):
        self._client = client
        self._project = project
        self._raw_info = raw_info

    @property
    def description(self) -> str:
        """Registered Model description."""
        return self._raw_info.description

    @property
    def name(self) -> str:
        """Registered Model display name."""
        return self._raw_info.display_name

    @property
    def owner(self) -> str:
        """Model owner name."""
        return self._client._get_username(self._raw_info.created_by)

    @property
    def uid(self) -> str:
        """Registered Model unique ID"""
        return self._raw_info.id

    def delete(self) -> None:
        """Delete Registered Model from the Project in H2O MLOps.
        This deletes the registered model and all its associated versions.
        """
        self._client._backend.storage.registered_model.delete_registered_model(
            h2o_mlops_autogen.StorageDeleteRegisteredModelRequest(self.uid)
        )

    def get_experiment(
        self, model_version: Union[int, str] = "latest"
    ) -> _experiments.MLOpsExperiment:
        """Get the Experiment object registered to an H2O MLOps Model Version.

        Args:
            model_version: Model Version number of the Experiment. Use "latest"
                to get the Experiment object of the latest Model Version.
        """
        if model_version == "latest":
            experiment_uid = self.versions()[0]["experiment_uid"]
        elif isinstance(model_version, int):
            experiment_uid = self.versions(version=model_version)[0]["experiment_uid"]
        else:
            raise RuntimeError("`model_version` value not accepted.")
        return self._project.experiments.get(experiment_uid)

    def register(self, experiment: _experiments.MLOpsExperiment) -> None:
        """Register an H2O MLOps Experiment to a Model Version.
        An Experiment can only be registered to one Model Version.

        Args:
            experiment: Experiment object to be registered
        """
        registered_model_version = h2o_mlops_autogen.StorageRegisteredModelVersion(
            registered_model_id=self.uid, experiment_id=experiment.uid
        )
        storage = self._client._backend.storage
        storage.registered_model_version.create_model_version(
            h2o_mlops_autogen.StorageCreateModelVersionRequest(
                registered_model_version=registered_model_version
            )
        )

    def unregister(self, experiment: _experiments.MLOpsExperiment) -> None:
        """Unregister an H2O MLOps Experiment from a Model Version.

        Args:
            experiment: Experiment object to be unregistered
        """
        version_uid = self.versions(experiment_uid=experiment.uid)[0]["uid"]
        self._client._backend.storage.registered_model_version.delete_model_version(
            h2o_mlops_autogen.StorageDeleteModelVersionRequest(
                id=version_uid,
            )
        )

    def versions(self, **selectors: Any) -> _utils.Table:
        """Retrieve Table of the H2O Registered Model's Versions and
        corresponding Experiment unique IDs.

        Examples::

            # filter on columns by using selectors
            model.versions(version=1)

            # use an index to get an H2O MLOps entity referenced by the table
            model_version = model.versions()[0]

            # get a new Table using multiple indexes or slices
            table = model.versions()[2,4]
            table = model.versions()[2:4]
        """
        storage = self._client._backend.storage
        model_versions = storage.registered_model_version.list_model_versions_for_model(
            h2o_mlops_autogen.StorageListModelVersionsForModelRequest(
                registered_model_id=self.uid
            )
        ).model_versions
        data = [
            {"version": m.version, "uid": m.id, "experiment_uid": m.experiment_id}
            for m in model_versions
        ]
        data.sort(key=lambda x: x["version"], reverse=True)
        return _utils.Table(
            data=data,
            keys=["version", "uid", "experiment_uid"],
            get_method=None,
            **selectors,
        )


class MLOpsModels:
    def __init__(self, client: _core.Client, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def create(self, name: str, description: Optional[str] = None) -> MLOpsModel:
        """Create a Registered Model in H2O MLOps.

        Args:
            name: display name for Registered Model
            description: description of Registered Model
        """
        storage = self._client._backend.storage
        raw_info = storage.registered_model.create_registered_model(
            h2o_mlops_autogen.StorageCreateRegisteredModelRequest(
                registered_model=h2o_mlops_autogen.StorageRegisteredModel(
                    display_name=name,
                    description=description or "",
                    project_id=self._project.uid,
                )
            )
        ).registered_model
        return MLOpsModel(client=self._client, project=self._project, raw_info=raw_info)

    def get(self, uid: str) -> MLOpsModel:
        """Get the Registered Model object corresponding to an
        H2O MLOps Registered Model.

        Args:
            uid: H2O MLOps unique ID for the Registered Model.
        """
        srv = self._client._backend.storage.registered_model
        raw_info = srv.get_registered_model(
            h2o_mlops_autogen.StorageGetRegisteredModelRequest(model_id=uid)
        ).registered_model
        return MLOpsModel(client=self._client, project=self._project, raw_info=raw_info)

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of H2O Registered Models available in the Project.

        Examples::

            # filter on columns by using selectors
            project.models.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            model = project.models.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.models.list()[2,4]
            table = project.models.list()[2:4]
        """
        srv = self._client._backend.storage.registered_model
        registered_models = []
        response = srv.list_registered_models(
            h2o_mlops_autogen.StorageListRegisteredModelsRequest(
                project_id=self._project.uid
            )
        )
        registered_models += response.registered_models
        while response.paging:
            response = srv.list_registered_models(
                h2o_mlops_autogen.StorageListRegisteredModelsRequest(
                    project_id=self._project.uid,
                    paging=h2o_mlops_autogen.StoragePagingRequest(
                        page_token=response.paging.next_page_token
                    ),
                )
            )
            registered_models += response.registered_models
        data = [{"name": m.display_name, "uid": m.id} for m in registered_models]
        return _utils.Table(
            data=data,
            keys=["name", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
