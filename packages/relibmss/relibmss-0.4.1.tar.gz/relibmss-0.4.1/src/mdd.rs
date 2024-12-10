use dd::count::*;
use dd::mdd;
use std::cell::RefCell;
use std::rc::Rc;
use std::rc::Weak;

use dd::dot::Dot;
use dd::mtmdd2;
use dd::mtmdd2::build_from_rpn;
use dd::mtmdd2::gen_var;
use pyo3::exceptions::PyValueError;
use pyo3::pyclass;
use pyo3::pymethods;
use pyo3::PyResult;
use std::collections::HashMap;

use crate::interval::Interval;
use crate::mdd_algo;

#[pyclass(unsendable)]
pub struct MddMgr {
    mdd: Rc<RefCell<mtmdd2::MtMdd2<i64>>>,
    vars: HashMap<String, MddNode>,
}

#[pyclass(unsendable)]
#[derive(Clone, Debug)]
pub struct MddNode {
    parent: Weak<RefCell<mtmdd2::MtMdd2<i64>>>,
    node: mtmdd2::MtMdd2Node<i64>,
}

impl MddNode {
    fn new(parent: Rc<RefCell<mtmdd2::MtMdd2<i64>>>, node: mtmdd2::MtMdd2Node<i64>) -> Self {
        MddNode {
            parent: Rc::downgrade(&parent),
            node,
        }
    }
}

#[pymethods]
impl MddMgr {
    #[new]
    pub fn new() -> Self {
        MddMgr {
            mdd: Rc::new(RefCell::new(mtmdd2::MtMdd2::new())),
            vars: HashMap::new(),
        }
    }

    pub fn size(&self) -> (usize, usize, usize, usize) {
        self.mdd.borrow().size()
    }

    pub fn zero(&self) -> MddNode {
        MddNode::new(self.mdd.clone(), self.mdd.borrow().zero())
    }

    pub fn one(&self) -> MddNode {
        MddNode::new(self.mdd.clone(), self.mdd.borrow().one())
    }

    pub fn val(&self, value: i64) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let node = mdd.value(value);
        MddNode::new(self.mdd.clone(), node)
    }

    pub fn defvar(&mut self, label: &str, range: usize) -> MddNode {
        if let Some(node) = self.vars.get(label) {
            return node.clone();
        } else {
            let level = self.vars.len();
            let result = {
                let mut mdd = self.mdd.borrow_mut();
                let range_ = (0..range).map(|x| x as i64).collect::<Vec<_>>(); // TODO: it should be changed in gen_var
                let node = gen_var(&mut mdd, label, level, &range_);
                MddNode::new(self.mdd.clone(), node)
            };
            self.vars.insert(label.to_string(), result.clone());
            result
        }
    }

    pub fn var(&self, label: &str) -> Option<MddNode> {
        if let Some(node) = self.vars.get(label) {
            Some(node.clone())
        } else {
            None
        }
    }

    pub fn rpn(&mut self, rpn: &str, vars: HashMap<String, usize>) -> PyResult<MddNode> {
        let tokens = rpn
            .split_whitespace()
            .map(|x| {
                match x {
                    "+" => mtmdd2::Token::Add,
                    "-" => mtmdd2::Token::Sub,
                    "*" => mtmdd2::Token::Mul,
                    "/" => mtmdd2::Token::Div,
                    "==" => mtmdd2::Token::Eq,
                    "!=" => mtmdd2::Token::Neq,
                    "<" => mtmdd2::Token::Lt,
                    "<=" => mtmdd2::Token::Lte,
                    ">" => mtmdd2::Token::Gt,
                    ">=" => mtmdd2::Token::Gte,
                    "&&" => mtmdd2::Token::And,
                    "||" => mtmdd2::Token::Or,
                    "!" => mtmdd2::Token::Not,
                    "?" => mtmdd2::Token::IfElse,
                    "True" => {
                        let node = {
                            let mdd = self.mdd.borrow();
                            mdd.one()
                        };
                        mtmdd2::Token::Value(node)
                    }
                    "False" => {
                        let node = {
                            let mdd = self.mdd.borrow();
                            mdd.zero()
                        };
                        mtmdd2::Token::Value(node)
                    }
                    _ => {
                        // parse whether it is a number or a variable
                        match x.parse::<i64>() {
                            Ok(val) => {
                                let node = {
                                    let mut mdd = self.mdd.borrow_mut();
                                    mdd.value(val)
                                };
                                mtmdd2::Token::Value(node)
                            }
                            Err(_) => {
                                let result = self.vars.get(x);
                                if let Some(node) = result {
                                    mtmdd2::Token::Value(node.node.clone())
                                } else {
                                    match vars.get(x) {
                                        Some(range) => {
                                            let node = self.defvar(x, range.clone());
                                            mtmdd2::Token::Value(node.node.clone())
                                        }
                                        None => panic!("Unknown variable: {}", x),
                                    }
                                }
                            }
                        }
                    }
                }
            })
            .collect::<Vec<_>>();
        let mut mdd = self.mdd.borrow_mut();
        if let Ok(node) = build_from_rpn(&mut mdd, &tokens) {
            Ok(MddNode::new(self.mdd.clone(), node))
        } else {
            Err(PyValueError::new_err("Invalid expression"))
        }
    }

    pub fn _and(&mut self, nodes: Vec<MddNode>) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let xs = nodes.iter().map(|x| &x.node).collect::<Vec<_>>();
        let mut result = mdd.one();
        for node in xs {
            result = mdd.and(&result, &node);
        }
        MddNode::new(self.mdd.clone(), result)
    }

    pub fn _or(&mut self, nodes: Vec<MddNode>) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let xs = nodes.iter().map(|x| &x.node).collect::<Vec<_>>();
        let mut result = mdd.zero();
        for node in xs {
            result = mdd.or(&result, &node);
        }
        MddNode::new(self.mdd.clone(), result)
    }

    pub fn _not(&mut self, node: &MddNode) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let result = mdd.not(&node.node);
        MddNode::new(self.mdd.clone(), result)
    }

    pub fn ifelse(&mut self, cond: &MddNode, then: &MddNode, els: &MddNode) -> MddNode {
        let mut mdd = self.mdd.borrow_mut();
        let result = mdd.ifelse(&cond.node, &then.node, &els.node);
        MddNode::new(self.mdd.clone(), result)
    }
}

#[pymethods]
impl MddNode {
    pub fn dot(&self) -> String {
        self.node.dot_string()
    }

    fn add(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.add(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn sub(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.sub(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn mul(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.mul(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn div(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.div(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn eq(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.eq(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn ne(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.neq(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn lt(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.lt(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn le(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.lte(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn gt(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.gt(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn ge(&self, other: &MddNode) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.gte(&self.node, &other.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn value(&self, other: i64) -> MddNode {
        let mddmgr = self.parent.upgrade().unwrap();
        let mut mdd = mddmgr.borrow_mut();
        let node = mdd.value(other);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    fn boolean(&self, other: bool) -> MddNode {
        if other {
            let mddmgr = self.parent.upgrade().unwrap();
            let mdd = mddmgr.borrow();
            let node = mdd.one();
            MddNode::new(self.parent.upgrade().unwrap(), node)
        } else {
            let mddmgr = self.parent.upgrade().unwrap();
            let mdd = mddmgr.borrow();
            let node = mdd.zero();
            MddNode::new(self.parent.upgrade().unwrap(), node)
        }
    }

    fn prob(&mut self, pv: HashMap<String, Vec<f64>>) -> HashMap<i64, f64> {
        let mgr = self.parent.upgrade().unwrap();
        let mut mdd = mgr.borrow_mut();
        mdd_algo::mddprob(&mut mdd, &self.node, pv)
    }

    fn prob_interval(&mut self, pv: HashMap<String, Vec<Interval>>) -> HashMap<i64, Interval> {
        let mgr = self.parent.upgrade().unwrap();
        let mut mdd = mgr.borrow_mut();
        mdd_algo::mddprob(&mut mdd, &self.node, pv)
    }

    fn mvs(&mut self) -> MddNode {
        let mgr = self.parent.upgrade().unwrap();
        let mut mdd = mgr.borrow_mut();
        let node = mdd_algo::mddminsol(&mut mdd, &self.node);
        MddNode::new(self.parent.upgrade().unwrap(), node)
    }

    pub fn count(&self) -> (usize, u64) {
        match &self.node {
            mtmdd2::MtMdd2Node::Value(x) => {
                x.count()
            },
            mtmdd2::MtMdd2Node::Bool(x) => {
                x.count()
            },
            mtmdd2::MtMdd2Node::Undet => {
                (0, 0)
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mdd_mgr() {
        let mut mgr = MddMgr::new();
        let zero = mgr.zero();
        let one = mgr.one();
        let two = mgr.val(2);
        let mut vars = HashMap::new();
        vars.insert("x".to_string(), 3);
        vars.insert("y".to_string(), 3);
        vars.insert("z".to_string(), 3);
        // println!("vars: {:?}", mgr.vars.borrow());
        let rpn = "x y z + *";
        if let Ok(node) = mgr.rpn(rpn, vars) {
            println!("{}", node.dot());
        }
    }
}
