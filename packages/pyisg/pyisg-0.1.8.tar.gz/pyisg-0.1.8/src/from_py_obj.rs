use libisg::{Coord, Data, DataBounds};
use pyo3::prelude::*;

use crate::*;

// Notes, it reduces code base if trait impl specialization is introduced (RFC 1210)

impl<'a> FromPyObject<'a> for Wrapper<Header> {
    #[inline]
    fn extract_bound(ob: &Bound<'a, PyAny>) -> PyResult<Self> {
        let model_name = ob
            .get_item("model_name")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("model_name", "str | None"))?;
        let model_year = ob
            .get_item("model_year")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("model_year", "str | `None`"))?;
        let model_type = ob
            .get_item("model_type")
            .map_or(Ok(None), |obj| obj.extract::<Option<Wrapper<ModelType>>>())
            .map_err(|_| {
                type_error!(
                    "model_type",
                    "'gravimetric' | 'geometric' | 'hybrid' | None"
                )
            })?
            .map(Into::into);
        let data_type = ob
            .get_item("data_type")
            .map_or(Ok(None), |obj| obj.extract::<Option<Wrapper<DataType>>>())
            .map_err(|_| type_error!("data_type", "'geoid' | 'quasi-geoid' | None"))?
            .map(Into::into);
        let data_units = ob
            .get_item("data_units")
            .map_or(Ok(None), |obj| obj.extract::<Option<Wrapper<DataUnits>>>())
            .map_err(|_| type_error!("data_units", "'meters' | 'feet' | None"))?
            .map(Into::into);
        let data_format = ob
            .get_item("data_format")
            .map_err(|_| missing_key!("data_format"))?
            .extract::<Wrapper<DataFormat>>()
            .map_err(|_| type_error!("data_format", "'grid' | 'sparse'"))?
            .into();
        let data_ordering = ob
            .get_item("data_ordering")
            .map_or(Ok(None), |obj| {
                obj.extract::<Option<Wrapper<DataOrdering>>>()
            })
            .map_err(|_| {
                type_error!(
                    "data_ordering",
                    "'N-to-S, W-to-E' | 'lat, lon, N' | 'east, north, N' | 'N' | 'zeta' | None"
                )
            })?
            .map(Into::into);
        let ref_ellipsoid = ob
            .get_item("ref_ellipsoid")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("ref_ellipsoid", "str | None"))?;
        let ref_frame = ob
            .get_item("ref_frame")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("ref_frame", "str | None"))?;
        let height_datum = ob
            .get_item("height_datum")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("height_datum", "str | None"))?;
        let tide_system = ob
            .get_item("tide_system")
            .map_or(Ok(None), |obj| obj.extract::<Option<Wrapper<TideSystem>>>())
            .map_err(|_| {
                type_error!(
                    "tide_system",
                    "'tide-free' | 'mean-tide' | 'zero-tide' | None"
                )
            })?
            .map(Into::into);
        let coord_type = ob
            .get_item("coord_type")
            .map_err(|_| missing_key!("coord_type"))?
            .extract::<Wrapper<CoordType>>()
            .map_err(|_| type_error!("coord_type", "'geodetic' | 'projected'"))?
            .into();
        let coord_units = ob
            .get_item("coord_units")
            .map_err(|_| missing_key!("coord_units"))?
            .extract::<Wrapper<CoordUnits>>()
            .map_err(|_| type_error!("coord_units", "'dms' | 'deg' | 'meters' | 'feet'"))?
            .into();
        let map_projection = ob
            .get_item("map_projection")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("map_projection", "str | None"))?;
        #[allow(non_snake_case)]
        let EPSG_code = ob
            .get_item("EPSG_code")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| type_error!("EPSG_code", "str | None"))?;
        let nrows = ob
            .get_item("nrows")
            .map_err(|_| missing_key!("nrows"))?
            .extract()
            .map_err(|_| type_error!("nrows", "int (usize)"))?;
        let ncols = ob
            .get_item("ncols")
            .map_err(|_| missing_key!("ncols"))?
            .extract()
            .map_err(|_| type_error!("ncols", "int (usize)"))?;
        let nodata = ob
            .get_item("nodata")
            .map_or(Ok(None), |obj| obj.extract())
            .map_err(|_| SerError::new_err("unexpected type on `nodata`, expected float | None"))?;
        let creation_date = ob
            .get_item("creation_date")
            .map_or(Ok(None), |obj| {
                obj.extract::<Option<Wrapper<CreationDate>>>()
            })
            .map_err(|_| {
                type_error!(
                    "creation_date",
                    "{ year: int (u16), month: int (u8), day: int (u8) } | None"
                )
            })?
            .map(Into::into);
        #[allow(non_snake_case)]
        let ISG_format = ob
            .get_item("ISG_format")
            .map_err(|_| missing_key!("ISG_format"))?
            .extract()
            .map_err(|_| type_error!("ISG_format", "str | None"))?;

        let data_bounds = match coord_type {
            CoordType::Geodetic => {
                let lat_min = ob
                    .get_item("lat_min")
                    .map_err(|_| missing_key!("lat_min"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "lat_min",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let lat_max = ob
                    .get_item("lat_max")
                    .map_err(|_| missing_key!("lat_max"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "lat_max",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let lon_min = ob
                    .get_item("lon_min")
                    .map_err(|_| missing_key!("lon_min"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "lon_min",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let lon_max = ob
                    .get_item("lon_max")
                    .map_err(|_| missing_key!("lon_max"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "lon_max",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();

                match data_format {
                    DataFormat::Grid => {
                        let delta_lat = ob
                            .get_item("delta_lat")
                            .map_err(|_| missing_key!("delta_lat"))?
                            .extract::<Wrapper<Coord>>()
                            .map_err(|_| type_error!("delta_lat", "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"))?
                            .into();
                        let delta_lon = ob
                            .get_item("delta_lon")
                            .map_err(|_| missing_key!("delta_lon"))?
                            .extract::<Wrapper<Coord>>()
                            .map_err(|_| type_error!("delta_lon", "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"))?
                            .into();

                        DataBounds::GridGeodetic {
                            lat_min,
                            lat_max,
                            lon_min,
                            lon_max,
                            delta_lat,
                            delta_lon,
                        }
                    }
                    DataFormat::Sparse => DataBounds::SparseGeodetic {
                        lat_min,
                        lat_max,
                        lon_min,
                        lon_max,
                    },
                }
            }
            CoordType::Projected => {
                let north_min = ob
                    .get_item("north_min")
                    .map_err(|_| missing_key!("north_min"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "north_min",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let north_max = ob
                    .get_item("north_max")
                    .map_err(|_| missing_key!("north_max"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "north_max",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let east_min = ob
                    .get_item("east_min")
                    .map_err(|_| missing_key!("east_min"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "east_min",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();
                let east_max = ob
                    .get_item("east_max")
                    .map_err(|_| missing_key!("east_max"))?
                    .extract::<Wrapper<Coord>>()
                    .map_err(|_| {
                        type_error!(
                            "east_max",
                            "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"
                        )
                    })?
                    .into();

                match data_format {
                    DataFormat::Grid => {
                        let delta_north = ob
                            .get_item("delta_north")
                            .map_err(|_| missing_key!("delta_north"))?
                            .extract::<Wrapper<Coord>>()
                            .map_err(|_| type_error!("delta_north", "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"))?
                            .into();
                        let delta_east = ob
                            .get_item("delta_east")
                            .map_err(|_| missing_key!("delta_east"))?
                            .extract::<Wrapper<Coord>>()
                            .map_err(|_| type_error!("delta_east", "float | { degree: int (i16), minutes: int (u8), second: int (u8) }"))?
                            .into();

                        DataBounds::GridProjected {
                            north_min,
                            north_max,
                            east_min,
                            east_max,
                            delta_north,
                            delta_east,
                        }
                    }
                    DataFormat::Sparse => DataBounds::SparseProjected {
                        north_min,
                        north_max,
                        east_min,
                        east_max,
                    },
                }
            }
        };

        Ok(Self(Header {
            model_name,
            model_year,
            model_type,
            data_type,
            data_units,
            data_format,
            data_ordering,
            ref_ellipsoid,
            ref_frame,
            height_datum,
            tide_system,
            coord_type,
            coord_units,
            map_projection,
            EPSG_code,
            data_bounds,
            nrows,
            ncols,
            nodata,
            creation_date,
            ISG_format,
        }))
    }
}

impl Wrapper<Data> {
    #[inline]
    pub(crate) fn extract_bound(ob: &Bound<PyAny>, header: &Header) -> PyResult<Self> {
        match header.data_format {
            DataFormat::Grid => {
                if let Ok(data) = ob.extract() {
                    Ok(Wrapper(Data::Grid(data)))
                } else {
                    Err(type_error!("data", "list[list[float | None]]"))
                }
            }
            DataFormat::Sparse => {
                if let Ok(data) = ob.extract::<Vec<(Wrapper<Coord>, Wrapper<Coord>, f64)>>() {
                    let r = data
                        .into_iter()
                        .map(|(a, b, c)| (a.into(), b.into(), c))
                        .collect();
                    Ok(Wrapper(Data::Sparse(r)))
                } else {
                    Err(type_error!(
                        "data",
                        "list[tuple[float | { degree: int (i16), minutes: int (u8), second: int (u8) }, float | { degree: int (i16), minutes: int (u8), second: int (u8) }, float]]"
                    ))
                }
            }
        }
    }
}

macro_rules! impl_from_py_object {
    ($type:tt) => {
        impl<'a> FromPyObject<'a> for Wrapper<$type> {
            #[inline]
            fn extract_bound(ob: &Bound<'a, PyAny>) -> PyResult<Self> {
                let r = ob
                    .extract::<String>()?
                    .parse()
                    .map_err(|_| PyValueError::new_err("unexpected value"))?;

                Ok(Self(r))
            }
        }
    };
}

impl_from_py_object!(ModelType);
impl_from_py_object!(DataType);
impl_from_py_object!(DataUnits);
impl_from_py_object!(DataFormat);
impl_from_py_object!(DataOrdering);
impl_from_py_object!(TideSystem);
impl_from_py_object!(CoordType);
impl_from_py_object!(CoordUnits);

impl<'a> FromPyObject<'a> for Wrapper<CreationDate> {
    #[inline]
    fn extract_bound(ob: &Bound<'a, PyAny>) -> PyResult<Self> {
        let year = ob.get_item("year")?.extract()?;
        let month = ob.get_item("month")?.extract()?;
        let day = ob.get_item("day")?.extract()?;

        Ok(Self(CreationDate::new(year, month, day)))
    }
}

impl<'a> FromPyObject<'a> for Wrapper<Coord> {
    fn extract_bound(ob: &Bound<'a, PyAny>) -> PyResult<Self> {
        if let Ok(v) = ob.extract() {
            Ok(Self(Coord::Dec(v)))
        } else {
            let deg = ob.get_item("degree")?.extract()?;
            let min = ob.get_item("minutes")?.extract()?;
            let sec = ob.get_item("second")?.extract()?;

            Ok(Self(Coord::with_dms(deg, min, sec)))
        }
    }
}
