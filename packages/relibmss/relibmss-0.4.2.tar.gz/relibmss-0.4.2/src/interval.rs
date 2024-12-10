use pyo3::prelude::*;
use std::ops::{Add, Div, Mul, Sub};

#[pyclass]
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Interval {
    #[pyo3(get, set)]
    pub lower: f64,
    #[pyo3(get, set)]
    pub upper: f64,
}

#[pymethods]
impl Interval {
    #[new]
    pub fn new(lower: f64, upper: f64) -> Self {
        if lower > upper {
            panic!("Lower bound cannot be greater than upper bound");
        }
        Interval { lower, upper }
    }

    pub fn __repr__(&self) -> PyResult<String> {
        Ok(format!("[{}, {}]", self.lower, self.upper))
    }
}

impl Add for Interval {
    type Output = Interval;

    fn add(self, other: Interval) -> Interval {
        Interval::new(self.lower + other.lower, self.upper + other.upper)
    }
}

impl Sub for Interval {
    type Output = Interval;

    fn sub(self, other: Interval) -> Interval {
        Interval::new(self.lower - other.upper, self.upper - other.lower)
    }
}

impl Mul for Interval {
    type Output = Interval;

    fn mul(self, other: Interval) -> Interval {
        let products = [
            self.lower * other.lower,
            self.lower * other.upper,
            self.upper * other.lower,
            self.upper * other.upper,
        ];
        Interval::new(
            products.iter().cloned().fold(f64::INFINITY, f64::min),
            products.iter().cloned().fold(f64::NEG_INFINITY, f64::max),
        )
    }
}

impl Div for Interval {
    type Output = Interval;

    fn div(self, other: Interval) -> Interval {
        if other.lower <= 0.0 && other.upper >= 0.0 {
            panic!("Division by an interval containing zero is not allowed");
        }
        let reciprocals = [1.0 / other.lower, 1.0 / other.upper];
        let reciprocal_interval = Interval::new(
            reciprocals.iter().cloned().fold(f64::INFINITY, f64::min),
            reciprocals
                .iter()
                .cloned()
                .fold(f64::NEG_INFINITY, f64::max),
        );
        self * reciprocal_interval
    }
}

impl From<f64> for Interval {
    fn from(value: f64) -> Self {
        Interval::new(value, value)
    }
}
