use pyo3::{pymodule, types::PyModule, PyResult, Python};

pub mod interval;

pub mod bdd;
pub mod bdd_algo;
pub mod mdd;
pub mod mdd_algo;

#[pymodule]
pub fn relibmss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<bdd::BddNode>()?;
    m.add_class::<bdd::BddMgr>()?;
    m.add_class::<mdd::MddNode>()?;
    m.add_class::<mdd::MddMgr>()?;
    m.add_class::<interval::Interval>()?;
    Ok(())
}
