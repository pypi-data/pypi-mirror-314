use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok("".to_string() + "+>> Result: [" + &(a + b).to_string() + "] <<")
}

/// Custom dictionary
#[pyclass(extends=PyDict)]
struct DoDict {
    something: i32,
}

#[pymethods]
impl DoDict {
    #[new]
    #[pyo3(signature = (*_args, **_kwargs))]
    fn new(_args: &Bound<'_, PyAny>, _kwargs: Option<&Bound<'_, PyAny>>) -> Self {
        Self { something: 0 }
    }
    fn get(&self) -> PyResult<i32> {
        Ok(self.something)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustdict(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<DoDict>()?;
    Ok(())
}
