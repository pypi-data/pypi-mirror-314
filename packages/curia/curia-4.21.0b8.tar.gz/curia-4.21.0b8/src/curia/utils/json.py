import dataclasses
import datetime
import enum
from typing import Any

import numpy as np
import pandas as pd
from numbers import Integral, Real


def pandas_isnull(obj):
    """
    Helper function to check if an object is null, even if it's a pandas object.
    """
    try:
        return pd.isnull(obj) is True  # prevents issues with pandas arrays treating this as an array
    except ValueError:
        return False


def nonrecursive_dataclass_unpack(dc: Any) -> dict:
    """
    Helper function to unpack a dataclass into a dict, without recursing into other dataclasses. This is useful as we
    want to use custom serialization for the dataclasses (annotating with the dataclass name) but dataclasses.asdict
    will recurse into inner dataclasses and make them indistinguishable from ordinary dicts. This function performs
    the
    """
    return {field.name: getattr(dc, field.name) for field in dataclasses.fields(dc)}


def sanitize(obj, n_digits=5):  # pylint: disable=R0911, R0912
    """
    Sanitizes obj into something json-encodable, and rounds floats to n_digits
    Args:
        obj: Object to sanitize
        n_digits: number of digits to round floats to

    Returns:
        Sanitized version of object.
    """
    if obj is None:
        return "NA"
    if pandas_isnull(obj):
        return "NA"
    if isinstance(obj, Integral):
        return int(obj)
    if isinstance(obj, Real):
        if obj == float("inf"):
            return "inf"
        if obj == float("-inf"):
            return "-inf"
        return round(float(obj), ndigits=n_digits)
    if isinstance(obj, enum.Enum):
        return sanitize(obj.value, n_digits=n_digits)
    if isinstance(obj, np.ndarray):
        return sanitize(obj.tolist(), n_digits=n_digits)
    if isinstance(obj, (bool, bytes, str, int, float)):
        return obj
    if isinstance(obj, list):
        return [sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj]
    if isinstance(obj, tuple):
        return tuple(sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj)
    if isinstance(obj, set):
        return {sanitize(sub_obj, n_digits=n_digits) for sub_obj in obj}
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        obj_dict = obj
        return {sanitize(key, n_digits=n_digits): sanitize(val, n_digits=n_digits) for key, val in obj_dict.items()}
    if dataclasses.is_dataclass(obj):
        return sanitize({'dataclass': type(obj).__name__, **nonrecursive_dataclass_unpack(obj)}, n_digits=n_digits)
    if isinstance(obj, pd.Series):
        return sanitize(list(obj), n_digits=n_digits)
    if isinstance(obj, pd.DataFrame):
        return sanitize(obj.to_dict(orient='records'), n_digits=n_digits)
    raise ValueError(f"Sanitizing value {obj} of type {type(obj)} is not supported. Add code to this function "
                     f"to support sanitization if necessary.")
