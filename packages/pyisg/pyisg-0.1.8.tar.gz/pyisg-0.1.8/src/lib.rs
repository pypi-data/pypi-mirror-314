use libisg::{
    CoordType, CoordUnits, CreationDate, Data, DataFormat, DataOrdering, DataType, DataUnits,
    Header, ModelType, TideSystem, ISG,
};
use pyo3::create_exception;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;

mod from_py_obj;
mod into;
mod to_py_obj;

macro_rules! type_error {
    ($name:expr, $expected:expr) => {
        SerError::new_err(concat!(
            "unexpected type on `",
            $name,
            "`, expected ",
            $expected
        ))
    };
}
macro_rules! missing_key {
    ($key:expr) => {
        SerError::new_err(concat!("missing key: '", $key, "'"))
    };
}

use missing_key;
use type_error;

struct Wrapper<T>(T);

// SerError and DeError are for propagates error message to Python side,
// Python code captures all them.
// This start makes code mess (see from_py_obj.rs),
// but it is conservative on error.

create_exception!(pyisg, SerError, PyValueError);
create_exception!(pyisg, DeError, PyValueError);

#[pyfunction]
fn loads<'a>(py: Python<'a>, s: &str) -> PyResult<Bound<'a, PyDict>> {
    let isg = libisg::from_str(s).map_err(|e| DeError::new_err(e.to_string()))?;

    let dict = PyDict::new(py);

    dict.set_item("comment", isg.comment)?;
    dict.set_item("header", Wrapper::<Header>(isg.header))?;
    dict.set_item("data", Wrapper::<Data>(isg.data))?;

    Ok(dict)
}

#[pyfunction]
fn dumps(obj: Bound<PyAny>) -> PyResult<String> {
    let comment = obj
        .get_item("comment")
        .map_or(Ok("".to_string()), |o| o.extract())
        .map_err(|_| type_error!("comment", "str"))?;

    let header = obj
        .get_item("header")
        .map_err(|_| missing_key!("header"))?
        .extract::<Wrapper<Header>>()?
        .into();

    let temp = obj.get_item("data").map_err(|_| missing_key!("data"))?;
    let data = Wrapper::<Data>::extract_bound(&temp, &header)?.into();

    let isg = ISG {
        comment,
        header,
        data,
    };

    let s = isg.to_string();
    Ok(s)
}

#[pymodule]
#[pyo3(name = "rust_impl")]
fn pyisg(py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(loads, m)?)?;
    m.add_function(wrap_pyfunction!(dumps, m)?)?;

    m.add("SerError", py.get_type::<SerError>())?;
    m.add("DeError", py.get_type::<DeError>())?;

    Ok(())
}
