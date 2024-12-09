mod matrix;
use pyo3::prelude::*;


/// A Python module implemented in Rust.
#[pymodule]
fn algebraic_immunity_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<matrix::Matrix>()?;
    Ok(())
}
