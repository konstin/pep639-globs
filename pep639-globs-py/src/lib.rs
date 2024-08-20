use glob::Pattern;
use pep639_globs::parse_pep639_glob;
use pyo3::types::{PyModule, PyModuleMethods};
use pyo3::{create_exception, Python};
use pyo3::{pyclass, pymethods, pymodule, Bound, PyResult};

create_exception!(module, Pep639GlobError, pyo3::exceptions::PyValueError);

#[pyclass]
pub struct Pep639Glob(Pattern);

#[pymethods]
impl Pep639Glob {
    #[new]
    fn __new__(pattern: &str) -> PyResult<Self> {
        let pattern =
            parse_pep639_glob(&pattern).map_err(|err| Pep639GlobError::new_err(err.to_string()))?;
        Ok(Self(pattern))
    }

    fn matches(&self, text: &str) -> bool {
        self.0.matches(text)
    }
}

#[pymodule(name = "pep639_globs")]
fn pep639_globs_py(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Pep639Glob>()?;
    m.add("Pep639GlobError", py.get_type_bound::<Pep639GlobError>())?;
    Ok(())
}
