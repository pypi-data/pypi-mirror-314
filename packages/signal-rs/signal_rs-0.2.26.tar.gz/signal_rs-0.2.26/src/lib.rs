use pyo3::prelude::*;
//use numpy::PyArray1;
//use pyo3::types::PyList;

use pyo3::prelude::*;

#[pyfunction]
fn integral_calculation_rust(data: Vec<f64>, duration: Vec<f64>, p0001: f64) -> PyResult<f64> {
    if data.len() != duration.len() || data.len() < 2 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Input arrays must have the same length and contain at least 2 elements.",
        ));
    }

    let mut integral = 0.0;

    for i in 0..data.len() - 1 {
        let y1 = data[i] - p0001;
        let y2 = data[i + 1] - p0001;
        let x1 = duration[i];
        let x2 = duration[i + 1];

        if y1 >= 0.0 && y2 >= 0.0 {
            // Trapezoidal rule
            let area = (y1 + y2) * (x2 - x1) / 2.0;
            integral += area;
        }
    }
    Ok(integral)
}

#[pymodule]
fn signal_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(integral_calculation_rust, m)?)?;
    Ok(())
}

