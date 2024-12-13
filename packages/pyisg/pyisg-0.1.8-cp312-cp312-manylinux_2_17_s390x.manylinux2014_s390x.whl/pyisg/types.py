"""Provides definition of types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, Union

if TYPE_CHECKING:
    from typing_extensions import (
        Required,  # typing @ >= 3.11
        TypeAlias,  # typing @ >= 3.10
    )

__all__ = [
    "ISGFormatType",
    #
    "HeaderType",
    #
    "ModelTypeType",
    "DataTypeType",
    "DataUnitsType",
    "DataFormatType",
    "DataOrderingType",
    "TideSystemType",
    "CoordTypeType",
    "CoordUnitsType",
    "CreationDateType",
    "DmsCoordType",
    #
    "SparseData",
    "GridData",
]

ModelTypeType: TypeAlias = Literal["gravimetric", "geometric", "hybrid"]
DataTypeType: TypeAlias = Literal["geoid", "quasi-geoid"]
DataUnitsType: TypeAlias = Literal["meters", "feet"]
DataFormatType: TypeAlias = Literal["grid", "sparse"]
DataOrderingType: TypeAlias = Literal["N-to-S, W-to-E", "lat, lon, N", "east, north, N", "N", "zeta"]
TideSystemType: TypeAlias = Literal["tide-free", "mean-tide", "zero-tide"]
CoordTypeType: TypeAlias = Literal["geodetic", "projected"]
CoordUnitsType: TypeAlias = Literal["dms", "deg", "meters", "feet"]


class CreationDateType(TypedDict):
    """Type of creation date."""

    year: int
    month: int
    day: int


class DmsCoordType(TypedDict):
    """Type of DMS coordinate."""

    degree: int
    minutes: int
    second: int


CoordType: TypeAlias = Union[DmsCoordType, float]


class HeaderType(TypedDict, total=False):
    """Type of Header dict."""

    model_name: str | None
    model_year: str | None
    model_type: ModelTypeType | None
    data_type: DataTypeType | None
    data_units: DataUnitsType | None
    data_format: Required[DataFormatType]
    data_ordering: DataOrderingType | None
    ref_ellipsoid: str | None
    ref_frame: str | None
    height_datum: str | None
    tide_system: TideSystemType | None
    coord_type: Required[CoordTypeType]
    coord_units: Required[CoordUnitsType]
    map_projection: str | None
    EPSG_code: str | None
    lat_min: CoordType | None
    lat_max: CoordType | None
    north_min: CoordType | None
    north_max: CoordType | None
    lon_min: CoordType | None
    lon_max: CoordType | None
    east_min: CoordType | None
    east_max: CoordType | None
    delta_lat: CoordType | None
    delta_lon: CoordType | None
    delta_north: CoordType | None
    delta_east: CoordType | None
    nrows: Required[int]
    ncols: Required[int]
    nodata: float | None
    creation_date: CreationDateType | None
    ISG_format: Required[str]


SparseData: TypeAlias = list[tuple[CoordType, CoordType, float]]
GridData: TypeAlias = list[list[Union[float, None]]]


class ISGFormatType(TypedDict):
    """Type of ISG data dict."""

    comment: str
    header: HeaderType
    data: GridData | SparseData
