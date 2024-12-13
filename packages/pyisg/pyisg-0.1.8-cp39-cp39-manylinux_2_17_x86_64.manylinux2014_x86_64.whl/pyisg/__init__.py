"""Provides serialize/deserialize API of ISG 2.0 format."""

from __future__ import annotations

from typing import Any, TextIO

from . import types
from .types import ISGFormatType

try:
    from . import rust_impl  # type: ignore
except ImportError as e:
    raise NotImplementedError("`pyisg` does not support current python/platform") from e

__version__ = "0.1.8"

__all__ = [
    "types",
    #
    "ISGFormatType",
    #
    "loads",
    "load",
    "dumps",
    "dump",
    #
    "ISGEncodeError",
    "ISGDecodeError",
]


def loads(s: str) -> ISGFormatType:
    """Deserialize ISG 2.0 format :obj:`str` obj to :obj:`dict` obj.

    Args:
        s: ISG 2.0 format :obj:`str` obj

    Returns:
        dict of ISG data

    Raises:
        DeserializeError: deserialization failed
    """
    try:
        return rust_impl.loads(s)
    except rust_impl.DeError as e:
        raise ISGDecodeError(*e.args) from None


def load(fp: TextIO) -> ISGFormatType:
    """Deserialize ISG 2.0 file-like obj to :obj:`dict` obj.

    Args:
        fp: file-like obj of ISG 2.0 format data

    Returns:
        dict of ISG data

    Raises:
        DeserializeError: deserialization failed
    """
    return loads(fp.read())


def dumps(obj: Any) -> str:
    """Serialize :class:`ISGFormatType`-like obj into :obj:`str` obj.

    Args:
        obj: :class:`ISGFormatType`-like obj (:obj:`Mapping`-like obj)

    Raises:
        SerializeError: serialization failed
        pyo3_runtime.PanicException: data has :obj:`None` even when nodata is :obj:`None`
    """
    try:
        return rust_impl.dumps(obj)
    except rust_impl.SerError as e:
        raise ISGEncodeError(*e.args) from None


def dump(obj: Any, fp: TextIO) -> int:
    """Serialize :class:`ISGFormatType` like obj  into file-like obj.

    Args:
        obj: :class:`ISGFormatType`-like obj (:obj:`Mapping`-like obj)
        fp: output file-like obj

    Returns:
        The number of characters written

    Raises:
        SerializeError: serialization failed
        pyo3_runtime.PanicException: data has :obj:`None` even when nodata is :obj:`None`
    """
    return fp.write(dumps(obj))


class ISGEncodeError(ValueError):
    """Error of :func:`dump` and :func:`dumps`."""

    pass


class ISGDecodeError(ValueError):
    """Error of :func:`load` and :func:`loads`."""

    pass
