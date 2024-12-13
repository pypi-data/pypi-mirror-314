use libisg::{Coord, Data, DataBounds, Header};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use std::convert::Infallible;

use crate::*;

impl<'py> IntoPyObject<'py> for Wrapper<Header> {
    type Target = PyDict;
    type Output = Bound<'py, Self::Target>;
    type Error = Infallible;

    #[inline]
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let dict = PyDict::new(py);

        macro_rules! set_item {
            ($field:ident) => {
                dict.set_item(stringify!($field), &self.0.$field)
                    .expect(concat!("fail to set `", stringify!($field), "` to dict"));
            };
        }

        macro_rules! set_item_as_string {
            ($field:ident) => {
                dict.set_item(stringify!($field), &self.0.$field.to_string())
                    .expect(concat!("fail to set `", stringify!($field), "` to dict"));
            };
        }

        macro_rules! set_item_opt_as_string {
            ($field:ident) => {
                dict.set_item(
                    stringify!($field),
                    &self.0.$field.as_ref().map(|v| v.to_string()),
                )
                .expect(concat!("fail to set `", stringify!($field), "` to dict"));
            };
        }

        macro_rules! set_item_data_bounds {
            ($field:ident) => {
                dict.set_item(stringify!($field), Wrapper::<Coord>($field))
                    .expect(concat!("fail to set `", stringify!($field), "` to dict"));
            };
        }

        macro_rules! set_item_data_bounds_none {
            ($field:ident) => {
                dict.set_item(stringify!($field), None::<Wrapper<Coord>>)
                    .expect(concat!("fail to set `", stringify!($field), "` to dict"));
            };
        }

        set_item!(model_name);
        set_item!(model_year);
        set_item_opt_as_string!(model_type);
        set_item_opt_as_string!(data_type);
        set_item_opt_as_string!(data_units);
        set_item_as_string!(data_format);
        set_item_opt_as_string!(data_ordering);
        set_item_opt_as_string!(ref_ellipsoid);
        set_item_opt_as_string!(ref_frame);
        set_item_opt_as_string!(height_datum);
        set_item_opt_as_string!(tide_system);
        set_item_as_string!(coord_type);
        set_item_as_string!(coord_units);
        set_item_opt_as_string!(map_projection);
        set_item_opt_as_string!(EPSG_code);
        match self.0.data_bounds {
            DataBounds::GridGeodetic {
                lat_min,
                lat_max,
                lon_min,
                lon_max,
                delta_lat,
                delta_lon,
            } => {
                set_item_data_bounds!(lat_min);
                set_item_data_bounds!(lat_max);
                set_item_data_bounds!(lon_min);
                set_item_data_bounds!(lon_max);
                set_item_data_bounds!(delta_lat);
                set_item_data_bounds!(delta_lon);
            }
            DataBounds::SparseGeodetic {
                lat_min,
                lat_max,
                lon_min,
                lon_max,
            } => {
                set_item_data_bounds!(lat_min);
                set_item_data_bounds!(lat_max);
                set_item_data_bounds!(lon_min);
                set_item_data_bounds!(lon_max);
                set_item_data_bounds_none!(delta_lat);
                set_item_data_bounds_none!(delta_lon);
            }
            DataBounds::GridProjected {
                north_min,
                north_max,
                east_min,
                east_max,
                delta_north,
                delta_east,
            } => {
                set_item_data_bounds!(north_min);
                set_item_data_bounds!(north_max);
                set_item_data_bounds!(east_min);
                set_item_data_bounds!(east_max);
                set_item_data_bounds!(delta_north);
                set_item_data_bounds!(delta_east);
            }
            DataBounds::SparseProjected {
                north_min,
                north_max,
                east_min,
                east_max,
            } => {
                set_item_data_bounds!(north_min);
                set_item_data_bounds!(north_max);
                set_item_data_bounds!(east_min);
                set_item_data_bounds!(east_max);
                set_item_data_bounds_none!(delta_north);
                set_item_data_bounds_none!(delta_east);
            }
        }
        set_item!(nrows);
        set_item!(ncols);
        set_item!(nodata);
        dict.set_item(
            "creation_date",
            self.0.creation_date.map(Wrapper::<CreationDate>),
        )
        .expect("fail to set `creation_date` to dict");
        set_item!(ISG_format);

        dict.into_pyobject(py)
    }
}

impl<'py> IntoPyObject<'py> for Wrapper<Data> {
    type Target = PyList;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    #[inline]
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match &self.0 {
            Data::Grid(data) => PyList::new(py, data)?
                .into_pyobject(py)
                .map_err(PyErr::from),
            Data::Sparse(data) => PyList::new(
                py,
                data.iter()
                    .map(|row| (Wrapper::<Coord>(row.0), Wrapper::<Coord>(row.1), row.2)),
            )?
            .into_pyobject(py)
            .map_err(PyErr::from),
        }
    }
}

impl<'py> IntoPyObject<'py> for Wrapper<CreationDate> {
    type Target = PyDict;
    type Output = Bound<'py, Self::Target>;
    type Error = Infallible;

    #[inline]
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let dict = PyDict::new(py);

        dict.set_item("year", self.0.year)
            .expect("fail to set `year` to dict");
        dict.set_item("month", self.0.month)
            .expect("fail to set `month` to dict");
        dict.set_item("day", self.0.day)
            .expect("fail to set `day` to dict");

        dict.into_pyobject(py)
    }
}

impl<'py> IntoPyObject<'py> for Wrapper<Coord> {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = Infallible;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self.0 {
            Coord::DMS {
                degree,
                minutes,
                second,
            } => {
                let dict = PyDict::new(py);

                dict.set_item("degree", degree)
                    .expect("fail to set `degree` to dict");
                dict.set_item("minutes", minutes)
                    .expect("fail to set `minutes` to dict");
                dict.set_item("second", second)
                    .expect("fail to set `second` to dict");

                dict.into_pyobject(py).map(|v| v.into_any())
            }

            Coord::Dec(v) => v.into_pyobject(py).map(|v| v.into_any()),
        }
    }
}
