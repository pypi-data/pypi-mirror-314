from collections.abc import Sequence
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import tabulate

import h2o_mlops_autogen
from h2o_mlops.options import SecurityOptions


class Table(Sequence):
    """Table that lazy loads."""

    def __init__(
        self,
        data: List[Dict[str, Any]],
        keys: List[str],
        get_method: Optional[Callable],
        **filters: Any,
    ):
        self._data = []
        self._keys = keys
        self._get = get_method

        for d in data:
            if all([d[k] == v for k, v in filters.items()]):
                self._data.append(d)

    def __getitem__(self, index: Union[int, slice, tuple]) -> Any:
        if isinstance(index, int):
            if self._get is not None:
                return self._get(self._data[index])
            return self._data[index]
        if isinstance(index, slice):
            return Table(self._data[index], self._keys, self._get)
        if isinstance(index, tuple):
            return Table([self._data[i] for i in index], self._keys, self._get)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        headers = [""] + self._keys
        table = [[i] + [d[key] for key in self._keys] for i, d in enumerate(self._data)]
        return tabulate.tabulate(table, headers=headers, tablefmt="presto")


def _convert_metadata(metadata: Any) -> Any:
    """Converts extracted metadata into Storage compatible value objects."""
    values = {}
    for k, v in metadata.values.items():
        o = h2o_mlops_autogen.StorageValue(
            bool_value=v.bool_value,
            double_value=v.double_value,
            duration_value=v.duration_value,
            int64_value=v.int64_value,
            string_value=v.string_value,
            json_value=v.json_value,
            timestamp_value=v.timestamp_value,
        )
        values[k] = o

    return h2o_mlops_autogen.StorageMetadata(values=values)


def _detect_passphrase_hash_type(security_options: SecurityOptions) -> Optional[str]:
    if not security_options.passphrase:
        return None
    if security_options.hashed_passphrase:
        if security_options._is_bcrypt_hash:
            return h2o_mlops_autogen.DeployPassphraseHashSecurityType.BCRYPT
        elif security_options._is_pbkdf2_hash:
            return h2o_mlops_autogen.DeployPassphraseHashSecurityType.PBKDF2
        else:
            raise ValueError(
                "Undetectable passphrase hash type. Expected a bcrypt or PBKDF2 hash."
            )
    return h2o_mlops_autogen.DeployPassphraseHashSecurityType.PLAINTEXT
