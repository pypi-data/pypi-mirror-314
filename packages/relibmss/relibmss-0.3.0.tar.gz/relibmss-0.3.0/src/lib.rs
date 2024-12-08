use pyo3::{pymodule, types::PyModule, PyResult, Python};

pub mod ft;
pub mod bdd;

pub mod interval;

pub mod mdd;

//pub mod pymod;

#[pymodule]
pub fn relibmss(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<bdd::BddNode>()?;
    m.add_class::<bdd::BddMgr>()?;
    m.add_class::<mdd::MddNode>()?;
    m.add_class::<mdd::MddMgr>()?;
    m.add_class::<interval::Interval>()?;
    Ok(())
}
