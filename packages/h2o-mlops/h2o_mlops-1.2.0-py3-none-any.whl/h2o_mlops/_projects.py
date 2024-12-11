from __future__ import annotations

from typing import Any
from typing import Optional

import h2o_mlops_autogen
from h2o_mlops import _batch_scoring_jobs
from h2o_mlops import _core
from h2o_mlops import _environments
from h2o_mlops import _experiments
from h2o_mlops import _models
from h2o_mlops import _utils


class MLOpsProject:
    def __init__(self, client: _core.Client, raw_info: Any):
        self._client = client
        self._raw_info = raw_info

    @property
    def description(self) -> str:
        """Project description."""
        return self._raw_info.description

    @property
    def environments(
        self,
    ) -> _environments.MLOpsEnvironments:
        """Environments available in the Project."""
        return _environments.MLOpsEnvironments(self._client, self)

    @property
    def experiments(self) -> _experiments.MLOpsExperiments:
        """Experiments linked to the Project."""
        return _experiments.MLOpsExperiments(self._client, self)

    @property
    def models(self) -> _models.MLOpsModels:
        """Registered Models in the Project."""
        return _models.MLOpsModels(self._client, self)

    @property
    def batch_scoring_jobs(self) -> _batch_scoring_jobs.MLOpsBatchScoringJobs:
        """Batch scoring jobs in the Project."""
        return _batch_scoring_jobs.MLOpsBatchScoringJobs(self._client, self)

    @property
    def name(self) -> str:
        """Project display name."""
        return self._raw_info.display_name

    @property
    def owner(self) -> str:
        """Project owner name."""
        return self._client._get_username(self._raw_info.owner_id)

    @property
    def tags(self) -> MLOpsProjectTags:
        """Manage Tags for the Project."""
        return MLOpsProjectTags(self._client, self)

    @property
    def uid(self) -> str:
        """Project unique ID."""
        return self._raw_info.id

    def delete(self) -> None:
        """Delete Project from H2O MLOps."""
        self._client._backend.storage.project.delete_project(
            h2o_mlops_autogen.StorageDeleteProjectRequest(project_id=self.uid)
        )


class MLOpsProjects:
    def __init__(self, client: _core.Client):
        self._client = client

    def create(self, name: str, description: Optional[str] = None) -> MLOpsProject:
        """Create a Project in H2O MLOps.

        Args:
            name: display name for Project
            description: description of Project
        """
        uid = self._client._backend.storage.project.create_project(
            h2o_mlops_autogen.StorageCreateProjectRequest(
                project=h2o_mlops_autogen.StorageProject(
                    display_name=name, description=description
                )
            )
        ).project.id
        return self.get(uid)

    def get(self, uid: str) -> MLOpsProject:
        """Get the Project object corresponding to a Project in H2O MLOps.

        Args:
            uid: H2O MLOps unique ID for the Project.
        """
        return MLOpsProject(
            self._client,
            self._client._backend.storage.project.get_project(
                h2o_mlops_autogen.StorageGetProjectRequest(project_id=uid)
            ).project,
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Projects available to the user.

        Examples::

            # filter on columns by using selectors
            mlops.projects.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            project = mlops.projects.list()[0]

            # get a new Table using multiple indexes or slices
            table = mlops.projects.list()[2,4]
            table = mlops.projects.list()[2:4]
        """
        projects = []
        response = self._client._backend.storage.project.list_projects(
            h2o_mlops_autogen.StorageListProjectsRequest()
        )
        projects += response.project
        while response.paging:
            response = self._client._backend.storage.project.list_projects(
                h2o_mlops_autogen.StorageListProjectsRequest(
                    paging=h2o_mlops_autogen.StoragePagingRequest(
                        page_token=response.paging.next_page_token
                    ),
                )
            )
            projects += response.project
        data = [{"name": p.display_name, "uid": p.id} for p in projects]
        return _utils.Table(
            data=data,
            keys=["name", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )


class MLOpsProjectTag:
    def __init__(self, client: _core.Client, project: MLOpsProject, raw_info: Any):
        self._client = client
        self._project = project
        self._raw_info = raw_info

    @property
    def label(self) -> str:
        """Text displayed by the Tag."""
        return self._raw_info["label"]

    @property
    def project(self) -> MLOpsProject:
        """Project the Tag belongs to."""
        return self._project

    @property
    def uid(self) -> str:
        """Tag unique ID."""
        return self._raw_info["uid"]

    def delete(self) -> None:
        """Delete Tag from the Project it belongs to."""
        raise NotImplementedError("Deleting Tags is not supported at this time.")


class MLOpsProjectTags:
    def __init__(self, client: _core.Client, project: Any):
        self._client = client
        self._project = project

    def create(self, label: str) -> MLOpsProjectTag:
        """Create a Tag for the Project.

        Args:
            label: text displayed by the Tag.
        """
        tag = self._client._backend.storage.tag.create_tag(
            h2o_mlops_autogen.StorageCreateTagRequest(
                tag=h2o_mlops_autogen.StorageTag(display_name=label),
                project_id=self._project.uid,
            )
        ).tag
        return MLOpsProjectTag(
            self._client, self._project, dict(label=tag.display_name, uid=tag.id)
        )

    def get_or_create(self, label: str) -> MLOpsProjectTag:
        """Get if exists, otherwise create, a Tag for the Project and return a
        corresponding Tag object.

        Args:
            label: text displayed by the Tag.
        """
        query = h2o_mlops_autogen.StorageQuery(
            clause=[
                h2o_mlops_autogen.StorageClause(
                    property_constraint=[
                        h2o_mlops_autogen.StoragePropertyConstraint(
                            _property=h2o_mlops_autogen.StorageProperty(
                                field="display_name"
                            ),
                            operator=h2o_mlops_autogen.StorageOperator.EQUAL_TO,
                            value=h2o_mlops_autogen.StorageValue(
                                string_value=label,
                            ),
                        )
                    ]
                )
            ]
        )
        tag = self._client._backend.storage.tag.list_tags(
            h2o_mlops_autogen.StorageListTagsRequest(
                filter=h2o_mlops_autogen.StorageFilterRequest(
                    query=query,
                ),
                project_id=self._project.uid,
            )
        ).tag
        if not tag:
            return self.create(label)
        return MLOpsProjectTag(
            self._client, self._project, dict(label=tag[0].display_name, uid=tag[0].id)
        )

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        """Retrieve Table of Tags available in the Project.

        Examples::

            # filter on columns by using selectors
            project.tags.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            tag = project.tags.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.tags.list()[2,4]
            table = project.tags.list()[2:4]
        """
        tags = []
        response = self._client._backend.storage.tag.list_tags(
            h2o_mlops_autogen.StorageListTagsRequest(project_id=self._project.uid)
        )
        tags += response.tag
        while response.paging:
            response = self._client._backend.storage.tag.list_tags(
                h2o_mlops_autogen.StorageListTagsRequest(
                    project_id=self._project.uid,
                    paging=h2o_mlops_autogen.StoragePagingRequest(
                        page_token=response.paging.next_page_token
                    ),
                )
            )
            tags += response.project
        tags = [t for t in tags if t.project_id == self._project.uid]
        data = [{"label": t.display_name, "uid": t.id} for t in tags]
        return _utils.Table(
            data=data,
            keys=["label"],
            get_method=lambda x: MLOpsProjectTag(self._client, self._project, x),
            **selectors,
        )
