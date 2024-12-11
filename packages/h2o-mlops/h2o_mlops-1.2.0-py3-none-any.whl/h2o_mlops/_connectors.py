from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from h2o_mlops import _core, _utils


@dataclass
class MLOpsBatchSourceSpec:
    uid: str
    name: str
    schema: str


@dataclass
class MLOpsBatchSinkSpec:
    uid: str
    name: str
    schema: str


class MLOpsBatchConnectors:

    def __init__(self, client: _core.Client):
        self._client = client

    @property
    def source_specs(self) -> MLOpsBatchSourceSpecs:
        return MLOpsBatchSourceSpecs(client=self._client)

    @property
    def sink_specs(self) -> MLOpsBatchSinkSpecs:
        return MLOpsBatchSinkSpecs(client=self._client)


class MLOpsBatchSourceSpecs:
    def __init__(self, client: _core.Client):
        self._client = client

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        source_specs = (
            self._client._backend.batch.source_spec.list_source_specs().source_specs
        )
        data_as_dicts = [
            {
                "name": source_spec.display_name,
                "uid": source_spec.name.split("/")[-1],
                "schema": source_spec.schema,
                "raw_info": source_spec,
            }
            for source_spec in source_specs
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "uid", "schema"],
            get_method=lambda x: MLOpsBatchSourceSpec(
                uid=x["uid"], name=x["name"], schema=x["schema"]
            ),
            **selectors,
        )


class MLOpsBatchSinkSpecs:
    def __init__(self, client: _core.Client):
        self._client = client

    def list(self, **selectors: Any) -> _utils.Table:  # noqa A003
        sink_specs = self._client._backend.batch.sink_spec.list_sink_specs().sink_specs
        data_as_dicts = [
            {
                "name": sink_spec.display_name,
                "uid": sink_spec.name.split("/")[-1],
                "schema": sink_spec.schema,
                "raw_info": sink_spec,
            }
            for sink_spec in sink_specs
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "uid", "schema"],
            get_method=lambda x: MLOpsBatchSinkSpec(
                uid=x["uid"], name=x["name"], schema=x["schema"]
            ),
            **selectors,
        )
