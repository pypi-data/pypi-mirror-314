from numbers import Number
from typing import Any, Dict, List

import numpy as np
import pandas as pd


def convert_to_np_dtype(dtype):
    if dtype == "Bool":
        return np.bool_
    elif dtype == "Int8":
        return np.int8
    elif dtype == "Int16":
        return np.int16
    elif dtype == "Int32":
        return np.int32
    elif dtype == "Int64":
        return np.int64
    elif dtype == "Uint8":
        return np.uint8
    elif dtype == "Uint16":
        return np.uint16
    elif dtype == "Uint32":
        return np.uint32
    elif dtype == "Uint64":
        return np.uint64
    elif dtype == "Half":
        return np.float16
    elif dtype == "Float" or "Double":
        return np.float64
    elif dtype == "Complex64":
        return np.complex64
    elif dtype == "Complex128":
        return np.complex128
    elif dtype == "BYTES":
        return np.bytes_
    return None


def to_nd_array_list(outputs: List[Dict[str, Any]]) -> List[np.ndarray]:
    res: List[np.ndarray] = []
    for output in outputs:
        if "dim" in output and output["dim"] is not None:
            res.append(
                np.ndarray(
                    shape=tuple(output["dim"]),
                    buffer=np.array(output["data"]),
                    dtype=convert_to_np_dtype(output["dtype"]),
                )
            )
        else:
            res.append(np.array(output["data"]))
    return res


def decode_inference_result(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Decode inference results. Since they have a potentially rich structure, this could become a substantial effort in the future.

    TODO: Support multiple outputs
    TODO: Support multiple data types
    """
    outputs = []
    i = -1
    for output in entry["outputs"]:
        i += 1
        # There are a few cases where we short circuit and append
        # in special cases, like Json types. We could use this for better
        # tensor field handling as well in the future.
        append_output = True
        try:
            first_output = entry["outputs"][i]
            first_type = next(iter(first_output.keys()))
        except Exception:
            raise RuntimeError(
                f"Missing output decoding inference response. entry: {entry}"
            )

        output = None
        known_types = {
            "Compact",
            "Half",
            "Float",
            "Double",
            "Uint8",
            "Int8",
            "Uint16",
            "Int16",
            "Uint32",
            "Int32",
            "Uint64",
            "Int64",
            "Complex64",
            "Complex128",
            "Bool",
            "String",
        }

        if first_type in known_types:
            output = first_output[first_type]
            output["dtype"] = first_type
        elif first_type == "Json":
            # If we can identify the tensor field, chase that down and return it
            try:
                if "tensor_fields" in first_output[first_type]["data"][0]:
                    field = first_output[first_type]["data"][0]["tensor_fields"][
                        0
                    ]  # 'tensor'
                    key = next(
                        iter(
                            first_output[first_type]["data"][0][field]["outputs"][
                                0
                            ].keys()
                        )
                    )  # Float
                    output = first_output[first_type]["data"][0][field]["outputs"][0][
                        key
                    ]
                    output["dtype"] = key
                # TODO: when Arrow changes are merged in, think of a better way of handling these edge or special cases.
                elif "tensor" in first_output[first_type]["data"][0]:
                    key = next(
                        iter(first_output[first_type]["data"][0]["tensor"][0].keys())
                    )  # Float
                    output = first_output[first_type]["data"][0]["tensor"][0][key]
                    output["dtype"] = key

            except Exception:
                pass

            if output is None:
                # No tensor field, try to parse keys in Json
                try:
                    nps = first_output[first_type]["data"][0]
                    dtype = None
                    for key, item in nps.items():
                        if key == "original":
                            dtype = next(iter(nps["original"]["outputs"][0].keys()))
                        else:
                            append_output = False
                            if isinstance(item, list) or np.isscalar(item):
                                data: Dict[str, Any] = {
                                    "dim": None,
                                    "data": item,
                                    "dtype": dtype,
                                }
                                outputs.append(data)
                            elif (
                                isinstance(item, dict)
                                and "dim" in item
                                and "data" in item
                            ):
                                item["dtype"] = dtype
                                outputs.append(item)
                            else:
                                raise RuntimeError(
                                    "Error parsing Json results for data. Supported ouput types are list, scalars for the data method, and dictionaries with a 'dim' key and a 'data' key"
                                )

                except Exception as ex:
                    raise RuntimeError(
                        f"Unexpected format decoding inference response. data: {entry} error: {ex}"
                    )
        else:
            raise RuntimeError(
                f"Unsupported type '{first_type}' in inference response. entry: {entry}"
            )
        # Post checks to make sure it looks like numpy
        if append_output and "dim" in output.keys() and "data" in output.keys():
            outputs.append(output)
        elif append_output:
            raise RuntimeError(f"Inference output does not look like numpy: {output}")

    return outputs


def flatten_tensor(prefix: str, numeric_list: list) -> Dict[str, Number]:
    """Converts a possibly multidimentionsl list of numbers into a
    dict where each item in the list is represented by a key value pair
    in the dict. Does not maintain dimensions since dataframes are 2d.
    Does not maintain/manage types since it should work for any type supported
    by numpy.

    For example
    [1,2,3] => {prefix_0: 1, prefix_1: 2, prefix_2: 3}.
    [[1,2],[3,4]] => {prefix_0_0: 1, prefix_0_1: 2, prefix_1_0: 3, prefix_1_1: 4}
    """
    output_dict = {}
    a = np.array(numeric_list).ravel()
    if not prefix.endswith("_"):
        prefix = prefix + "_"
    for i, v in enumerate(a):
        name = f"{prefix}{i}"
        output_dict[name] = v
    return output_dict


def flatten_dict(prefix: str, input_dict: Dict) -> Dict[str, Any]:
    """Recursively flattens the input dict, setting the values on the output dict.
    Assumes simple value types (str, numbers, dicts, and lists).
    If a value is a dict it is flattened recursively.
    If a value is a list each item is set as a new k, v pair.
    """

    output_dict = {}
    for k, v in input_dict.items():
        name = f"{prefix}{k}"
        if isinstance(v, list):
            if len(v) > 0:
                if isinstance(v[0], str):
                    for i, item in enumerate(v):
                        output_dict[f"{name}_{i}"] = item
                elif isinstance(v[0], (float, int, bool)):
                    output_dict.update(flatten_tensor(name + "_", v))
                else:
                    # Things like check_failures have nested structs
                    output_dict[name] = str(v)
                    # raise TypeError(f"Can't handle type {v_type} for key '{k}'")
            else:
                output_dict[name] = None
        elif isinstance(v, dict):
            output_dict.update(flatten_dict(name + "_", v))
        else:
            output_dict[name] = v
    return output_dict


def inference_logs_to_dataframe(logs: List[Dict[str, Any]]) -> pd.DataFrame:
    """Very similar to dict_list_to_dataframe but specific to inference
    logs since they have input and output heiararchical fields/structures
    that must be treated in particular ways."""

    def flatten_inputs(inputs: Dict[str, Any]):
        """Inputs/original_data is a dict of string to values of multi_dimensional
        list and need to have their own numbering to fit that. We should use the
        input name but for consistency we'll use 'input' (since the name is not
        available elsewhere)."""
        fo = {}
        for i, (_k, v) in enumerate(inputs.items()):
            # One day we may be able to use the tensor name
            # But for now we don't have or use that in the
            # assays so use 'input'
            fo.update(flatten_tensor(f"input_{i}", v))
        return fo

    def flatten_outputs(outputs: List[Dict[str, Dict[str, Any]]]) -> Dict[str, Any]:
        """The key piece of info we want from outputs is the nested 'data' field
        which could be a multi-dimensional list. This function pulls that out and
        numbers/names it appropriately."""
        fo = {}
        for i, output_dict in enumerate(outputs):  # loop through each output
            for _k, ov in output_dict.items():  # get 'data' for each output
                data = ov["data"]
                fo.update(flatten_tensor(f"output_{i}", data))

        return fo

    def process_inference_record(temp_log) -> Dict[str, Any]:
        """Manipulate an inference record dict and flatten it."""
        # Copy the log so we don't change the original
        temp_log = temp_log.copy()

        # Process and delete the inputs and outputs
        inputs = temp_log["original_data"]
        input_dict = flatten_inputs(inputs)
        del temp_log["original_data"]

        outputs = temp_log["outputs"]
        output_dict = flatten_outputs(outputs)
        del temp_log["outputs"]

        # Flatten the temp log (should be straightforward)
        # and add in the input and output dicts
        output_log = flatten_dict("", temp_log)
        output_log.update(input_dict)
        output_log.update(output_dict)

        return output_log

    processed_logs = [process_inference_record(log) for log in logs]

    df = pd.DataFrame(processed_logs)
    return df


def nested_df_to_flattened_df(orig: pd.DataFrame) -> pd.DataFrame:
    if len(orig) == 0:
        return orig

    def process_row(row: pd.Series) -> Dict[str, Any]:
        flattened_dict = {"time": row["time"], "metadata": row["metadata"]}

        for k, v in row["in"].items():
            flattened_dict.update(flatten_tensor(f"input_{k}", v))

        for k, v in row["out"].items():
            flattened_dict.update(flatten_tensor(f"output_{k}", v))

        return flattened_dict

    return pd.DataFrame(process_row(row) for _, row in orig.iterrows())


def dict_list_to_dataframe(assay_results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Primarily for assay result lists but can be used for any list of simple
    dicts."""
    res = [flatten_dict("", r) for r in assay_results]

    df = pd.DataFrame(res)
    return df
