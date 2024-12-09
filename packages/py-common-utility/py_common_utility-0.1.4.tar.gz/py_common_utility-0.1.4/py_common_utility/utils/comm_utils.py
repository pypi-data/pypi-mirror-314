import hashlib
import json
import os
import random
import string
import sys
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, TypeVar, List
from uuid import UUID

from py_common_utility.utils import time_utils


def dict_to_sha1(input_dict):
    # Serialize the dictionary to a JSON string
    json_str = json.dumps(input_dict, sort_keys=True)
    # Encode the JSON string into bytes
    json_bytes = json_str.encode('utf-8')
    # Compute the SHA-1 hash
    sha1_hash = hashlib.sha1(json_bytes).hexdigest()
    return sha1_hash


def get_memory_size(obj, seen=None) -> int:
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Mark as seen

    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_memory_size(v, seen) for v in obj.values()])
        size += sum([get_memory_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_memory_size(obj.__dict__, seen)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        size += sum([get_memory_size(i, seen) for i in obj])
    return size



def random_chars(count: int) -> str:
    letters = string.ascii_letters + string.digits
    oid = "".join(random.choice(letters) for i in range(count))
    return oid


E = TypeVar("E", bound=Enum)


def value_of_enum(e: E, v: Any) -> E:
    for enum_val in e:
        e: E = enum_val
        if e.value == v:
            return e
    raise KeyError("Not find :" + v)


def to_dict(obj, classkey=None) -> dict:
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            v = _to_date_dict(v)
            data[k] = to_dict(v, classkey)
        return data
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return time_utils.to_time_utc_iso(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    # elif hasattr(obj, '_ast'):
    #     return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if not callable(value) and not key.startswith("_"):
                data[key] = to_dict(value, classkey)
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


def _to_date_dict(v: Any) -> Any:
    if isinstance(v, datetime):
        return time_utils.to_time_utc_iso(v)
    return v


def to_sh256_str(plain: str) -> str:
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


def save_tmp_file(text: str) -> str:
    file = None
    completeName = None
    try:

        completeName = "/tmp/" + random_chars(32)
        os.makedirs(os.path.dirname(completeName), exist_ok=True)
        file = open(completeName, "wb")
        file.write(text.encode())
    finally:
        file.close()
    return completeName


def put_all_to_dict(src: dict, to: List[dict]) -> dict:
    for e in to:
        e.update(src)
    return src


def to_flat_dict_by_list(l: list, dot_sign=".") -> dict:
    ans = {}
    for idx, v in enumerate(l):
        if isinstance(v, list):
            child_flat_dict = to_flat_dict_by_list(v, dot_sign)
        if isinstance(v, dict):
            child_flat_dict = to_flat_dict(v, dot_sign)
        if child_flat_dict:
            for ck, cv in child_flat_dict.items():
                ans[f"{idx}{dot_sign}{ck}"] = cv
            break
        ans[str(idx)] = v
    return ans


def to_flat_dict(d: dict, dot_sign=".") -> dict:
    ans = {}
    for k, v in d.items():
        child_flat_dict = None
        if isinstance(v, list):
            child_flat_dict = to_flat_dict_by_list(v, dot_sign)
        if isinstance(v, dict):
            child_flat_dict = to_flat_dict(v, dot_sign)
        if child_flat_dict:
            for ck, cv in child_flat_dict.items():
                ans[f"{k}{dot_sign}{ck}"] = cv
            continue
        ans[k] = v
    return ans


def to_json_str(obj) -> str:
    obj_d = to_dict(obj)
    ans = json.dumps(obj_d)
    return ans
