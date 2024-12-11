from __future__ import annotations

from typing import Any

from h2o_mlops import _core
from h2o_mlops import _utils


class MLOpsRuntimes:
    def __init__(self, client: _core.Client):
        self._client = client

    @property
    def scoring(self) -> MLOpsScoringRuntimes:
        return MLOpsScoringRuntimes(client=self._client)


class MLOpsScoringRuntime:
    def __init__(self, raw_info: Any):
        self._raw_info = raw_info

    @property
    def artifact_type(self) -> str:
        return self._raw_info.deployable_artifact_type.name

    @property
    def name(self) -> str:
        return self._raw_info.runtime.display_name

    @property
    def uid(self) -> str:
        return self._raw_info.runtime.name


class MLOpsScoringRuntimes:
    def __init__(self, client: _core.Client):
        self._client = client

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        compositions = (
            self._client._backend.deployer.composition.list_artifact_compositions(
                {}
            ).artifact_composition
        )
        data = [
            {
                "name": c.runtime.display_name,
                "artifact_type": c.deployable_artifact_type.name,
                "uid": c.runtime.name,
                "raw_info": c,
            }
            for c in compositions
        ]
        return _utils.Table(
            data=data,
            keys=["name", "artifact_type", "uid"],
            get_method=lambda x: MLOpsScoringRuntime(x["raw_info"]),
            **selectors,
        )
