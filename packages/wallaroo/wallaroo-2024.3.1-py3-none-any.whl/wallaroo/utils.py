import functools
import os
from typing import Optional, TextIO, Union

import numpy as np
import pyarrow as pa  # type: ignore

ASSAYS_V2_ENABLED = "ASSAYS_V2_ENABLED"

DEFAULT_ARROW_FILE_SUFFIX = "arrow"
DEFAULT_JSON_FILE_SUFFIX = "json"


def is_assays_v2_enabled():
    return os.getenv(ASSAYS_V2_ENABLED, "false").lower() == "true"


def flatten_np_array_columns(df, col):
    if isinstance(df[col][0], np.ndarray):
        return df[col].apply(lambda x: np.array(x).ravel())
    else:
        return df[col]


def convert_ndarray_batch_to_arrow(arr):
    batch_size = arr.shape[0]
    inner_size = functools.reduce(lambda a, b: a * b, arr.shape[1:])
    offsets = range(0, (batch_size * inner_size) + 1, inner_size)
    return pa.ListArray.from_arrays(offsets, arr.reshape([batch_size * inner_size]))


def generate_file_name(
    directory: str, file_prefix: str, file_num: int, file_suffix: str
) -> str:
    return os.path.join(directory, f"{file_prefix}-{file_num}.{file_suffix}")


def create_new_arrow_file(
    directory: str, file_num: int, file_prefix: str, file_suffix: str, schema: pa.Schema
) -> pa.RecordBatchFileWriter:
    filepath = generate_file_name(directory, file_prefix, file_num, file_suffix)
    sink = pa.OSFile(filepath, "wb")
    writer = pa.ipc.new_file(sink, schema)
    return writer


def create_new_json_file(
    directory: str, file_num: int, file_prefix: str, file_suffix: str
) -> TextIO:
    filepath = generate_file_name(directory, file_prefix, file_num, file_suffix)
    sink = open(filepath, "w")
    return sink


def create_new_file(
    directory: str,
    file_num: int,
    file_prefix: str,
    schema: Optional[pa.Schema] = None,
    arrow: Optional[bool] = False,
) -> Union[pa.RecordBatchFileWriter, TextIO]:
    if arrow:
        return create_new_arrow_file(
            directory, file_num, file_prefix, DEFAULT_ARROW_FILE_SUFFIX, schema
        )
    else:
        return create_new_json_file(
            directory, file_num, file_prefix, DEFAULT_JSON_FILE_SUFFIX
        )


def write_to_file(
    record_batch: Union[pa.RecordBatch, str],
    writer: Union[pa.RecordBatchFileWriter, TextIO],
) -> None:
    if isinstance(record_batch, pa.RecordBatch):
        writer.write_batch(record_batch)  # type: ignore
    elif isinstance(record_batch, str):
        writer.write(record_batch)  # type: ignore
    else:
        raise TypeError(
            f"write_to_file() expects pa.RecordBatch or str, got {type(record_batch)}"
        )
