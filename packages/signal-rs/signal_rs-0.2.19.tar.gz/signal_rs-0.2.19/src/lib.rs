use pyo3::prelude::*;
//use numpy::PyArray1;
//use pyo3::types::PyList;

use pyo3::prelude::*;

#[pyfunction]
fn integral_calculation_rust(_py: Python) -> u64 {
    let integral = 1000;  // No need for mutability here
    integral
}

#[pymodule]
fn signal_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(integral_calculation_rust, m)?)?;
    Ok(())
}

