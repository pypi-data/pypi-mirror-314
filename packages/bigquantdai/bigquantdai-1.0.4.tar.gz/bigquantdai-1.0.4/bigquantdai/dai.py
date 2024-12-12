import json
from typing import Dict, List, Optional, Set, Tuple, Type, Union, Any
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds

from ._client import client_instance
from ._constant import READ_BDB_COMPATIBLE_DATA_TYPE, WRITE_BDB_COMPATIBLE_DATA_TYPE, OnDuplicates, DEFAULT_PARTITION_FIELD   # noqa: F401


def login(access_key: str, secret_key: str, host: str = "bigquant.com", port: int = 17010):
    """Authenticate with access_key and secret_key."""
    client_instance.login(access_key, secret_key, host=host, port=port)


def quota():
    """Get the quota information."""
    responses = client_instance.do_action("quota")
    results = [response.body.to_pybytes().decode("utf-8") for response in responses if response.body]
    if results:
        return json.loads(results[0])


class DataSource:
    id: str

    def __init__(self: "DataSource", id: str) -> None:
        self.id = id

    def __repr__(self):
        return f'dai.DataSource("{self.id}")'

    def read_bdb(
        self,
        as_type: Type[READ_BDB_COMPATIBLE_DATA_TYPE] = pa.Table,
        partition_filter: Optional[Dict[str, Union[tuple, set]]] = None,
        columns: Optional[List[str]] = None,
        **kwargs,
    ) -> READ_BDB_COMPATIBLE_DATA_TYPE:
        assert self.id

        return client_instance.read_bdb(
            self.id,
            as_type,
            partition_filter=partition_filter,
            columns=columns,
            **kwargs,
        )

    @classmethod
    def write_bdb(
        cls,
        data: WRITE_BDB_COMPATIBLE_DATA_TYPE,
        *,
        id: Optional[str] = None,
        partitioning: Optional[List[str]] = None,
        indexes: Optional[List[str]] = None,
        excludes: Optional[Set[str]] = None,
        unique_together: Optional[List[str]] = None,
        on_duplicates: OnDuplicates = OnDuplicates.last,
        sort_by: Optional[List[Tuple[str, str]]] = None,
        preserve_pandas_index=False,
        docs: Optional[Dict[str, Any]] = None,
        timeout: int = 300,
        extra: str = "",
        **kwargs,
    ) -> "DataSource":
        assert data is not None

        if isinstance(data, pd.DataFrame):
            data = pa.Table.from_pandas(data, preserve_index=preserve_pandas_index)
        elif isinstance(data, ds.Dataset):
            data = data.to_table()

        return cls(
            id=client_instance.write_bdb(
                data=data,
                id=id,
                partitioning=partitioning,
                indexes=indexes,
                excludes=excludes,
                unique_together=unique_together,
                on_duplicates=on_duplicates,
                sort_by=sort_by,
                docs=docs,
                timeout=timeout,
                extra=extra,
                **kwargs,
            )
        )

    def delete(self):
        assert self.id
        responses = client_instance.do_action("delete", self.id.encode("utf-8"))
        error_message = [response.body.to_pybytes().decode("utf-8") for response in responses if response.body]
        if error_message:
            raise Exception(",".join(error_message))
