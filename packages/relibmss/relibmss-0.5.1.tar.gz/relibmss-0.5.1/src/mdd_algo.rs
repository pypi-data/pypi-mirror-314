// mod ft

use std::collections::HashMap;
use std::ops::{Add, Mul, Sub};

use dd::common::NodeId;
use dd::{mdd, mtmdd};
use dd::mtmdd2;
use dd::nodes::NonTerminal;
use dd::nodes::Terminal;

pub fn mddprob<T>(
    mdd: &mut mtmdd2::MtMdd2<i64>,
    node: &mtmdd2::MtMdd2Node<i64>,
    pv: HashMap<String, Vec<T>>,
) -> HashMap<i64, T>
where
    T: Add<Output = T> + Sub<Output = T> + Mul<Output = T> + Clone + Copy + PartialEq + From<f64>,
{
    match node {
        mtmdd2::MtMdd2Node::Value(fnode) => {
            let mut cache = HashMap::new();
            vmddprob(&mut mdd.mtmdd_mut(), &fnode, &pv, &mut cache)
        },
        mtmdd2::MtMdd2Node::Bool(fnode) => {
            let mut cache = HashMap::new();
            bmddprob(&mut mdd.mdd_mut(), &fnode, &pv, &mut cache)
        },
        _ => panic!("The node should be either Value or Bool"),
    }
}

fn vmddprob<T>(
    mdd: &mut mtmdd::MtMdd<i64>,
    node: &mtmdd::MtMddNode<i64>,
    pv: &HashMap<String, Vec<T>>,
    cache: &mut HashMap<NodeId, HashMap<i64, T>>,
) -> HashMap<i64, T>
where
    T: Add<Output = T> + Sub<Output = T> + Mul<Output = T> + Clone + Copy + PartialEq + From<f64>,
{
    let key = node.id();
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                mtmdd::MtMddNode::Terminal(fnode) => {
                    let mut map = HashMap::new();
                    let value = fnode.value();
                    map.insert(value, T::from(1.0));
                    map
                }
                mtmdd::MtMddNode::NonTerminal(fnode) => {
                    let label = fnode.header().label();
                    let fp = pv.get(label).unwrap();
                    let mut map = HashMap::new();
                    for (i, x) in fnode.iter().enumerate() {
                        let tmp = vmddprob(mdd, &x, pv, cache);
                        for (k, v) in tmp.iter() {
                            let key = *k;
                            let value = *v;
                            let entry = map.entry(key).or_insert(T::from(0.0));
                            *entry = *entry + fp[i] * value;
                        }
                    }
                    map
                }
                mtmdd::MtMddNode::Undet => HashMap::new(),
            };
            cache.insert(key, result.clone());
            result
        }
    }
}

fn bmddprob<T>(
    mdd: &mut mdd::Mdd,
    node: &mdd::MddNode,
    pv: &HashMap<String, Vec<T>>,
    cache: &mut HashMap<NodeId, HashMap<i64, T>>,
) -> HashMap<i64, T>
where
    T: Add<Output = T> + Sub<Output = T> + Mul<Output = T> + Clone + Copy + PartialEq + From<f64>,
{
    let key = node.id();
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                mdd::MddNode::Zero => {
                    let mut map = HashMap::new();
                    let value = 0;
                    map.insert(value, T::from(1.0));
                    map
                },
                mdd::MddNode::One => {
                    let mut map = HashMap::new();
                    let value = 1;
                    map.insert(value, T::from(1.0));
                    map
                },
                mdd::MddNode::NonTerminal(fnode) => {
                    let label = fnode.header().label();
                    let fp = pv.get(label).unwrap();
                    let mut map = HashMap::new();
                    for (i, x) in fnode.iter().enumerate() {
                        let tmp = bmddprob(mdd, &x, pv, cache);
                        for (k, v) in tmp.iter() {
                            let key = *k;
                            let value = *v;
                            let entry = map.entry(key).or_insert(T::from(0.0));
                            *entry = *entry + fp[i] * value;
                        }
                    }
                    map
                },
                mdd::MddNode::Undet => HashMap::new(),
            };
            cache.insert(key, result.clone());
            result
        }
    }
}

pub fn mddminsol(
    mdd: &mut mtmdd2::MtMdd2<i64>,
    node: &mtmdd2::MtMdd2Node<i64>,
) -> mtmdd2::MtMdd2Node<i64> {
    match node {
        mtmdd2::MtMdd2Node::Value(fnode) => {
            let mut cache1 = HashMap::new();
            let mut cache2 = HashMap::new();
            let result = vmddminsol(&mut mdd.mtmdd_mut(), &fnode, &mut cache1, &mut cache2);
            mtmdd2::MtMdd2Node::Value(result)
        }
        mtmdd2::MtMdd2Node::Bool(fnode) => {
            let mut cache1 = HashMap::new();
            let mut cache2 = HashMap::new();
            let result = bmddminsol(&mut mdd.mdd_mut(), &fnode, &mut cache1, &mut cache2);
            mtmdd2::MtMdd2Node::Bool(result)
        }
        _ => panic!("The node should be either Value or Bool"),
    }
}

fn vmddminsol(
    dd: &mut mtmdd::MtMdd<i64>,
    node: &mtmdd::MtMddNode<i64>,
    cache1: &mut HashMap<NodeId, mtmdd::MtMddNode<i64>>,
    cache2: &mut HashMap<(NodeId, NodeId), mtmdd::MtMddNode<i64>>,
) -> mtmdd::MtMddNode<i64> {
    let key = node.id();
    match cache1.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                mtmdd::MtMddNode::Terminal(_) => node.clone(),
                mtmdd::MtMddNode::NonTerminal(fnode) => {
                    let mut result = Vec::new();
                    for (i, x) in fnode.iter().enumerate() {
                        if i == 0 {
                            let tmp = vmddminsol(dd, &x, cache1, cache2);
                            result.push(tmp);
                        } else {
                            let tmp = vmddminsol(dd, &x, cache1, cache2);
                            let tmp2 = vmdd_without(dd, &fnode[i - 1], &tmp, cache2);
                            result.push(tmp2);
                        }
                    }
                    dd.create_node(fnode.header(), &result)
                }
                mtmdd::MtMddNode::Undet => dd.undet(),
            };
            cache1.insert(key, result.clone());
            result
        }
    }
}

fn bmddminsol(
    dd: &mut mdd::Mdd,
    node: &mdd::MddNode,
    cache1: &mut HashMap<NodeId, mdd::MddNode>,
    cache2: &mut HashMap<(NodeId, NodeId), mdd::MddNode>,
) -> mdd::MddNode {
    let key = node.id();
    match cache1.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                mdd::MddNode::Zero => dd.undet(),
                mdd::MddNode::One => node.clone(),
                mdd::MddNode::NonTerminal(fnode) => {
                    let mut result = Vec::new();
                    for (i, x) in fnode.iter().enumerate() {
                        if i == 0 {
                            let tmp = bmddminsol(dd, &x, cache1, cache2);
                            result.push(tmp);
                        } else {
                            let tmp = bmddminsol(dd, &x, cache1, cache2);
                            let tmp2 = bmdd_without(dd, &fnode[i - 1], &tmp, cache2);
                            result.push(tmp2);
                        }
                    }
                    dd.create_node(fnode.header(), &result)
                }
                mdd::MddNode::Undet => dd.undet(),
            };
            cache1.insert(key, result.clone());
            result
        }
    }
}

fn vmdd_without(
    mdd: &mut mtmdd::MtMdd<i64>,
    f: &mtmdd::MtMddNode<i64>,
    g: &mtmdd::MtMddNode<i64>, // minsol tree
    cache: &mut HashMap<(NodeId, NodeId), mtmdd::MtMddNode<i64>>,
) -> mtmdd::MtMddNode<i64> {
    let key = (f.id(), g.id());
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match (f, g) {
                (mtmdd::MtMddNode::Undet, _) => g.clone(),
                (_, mtmdd::MtMddNode::Undet) => mdd.undet(),
                (mtmdd::MtMddNode::Terminal(fnode), mtmdd::MtMddNode::Terminal(gnode)) => {
                    if fnode.value() == gnode.value() {
                        mdd.undet()
                    } else {
                        g.clone()
                    }
                }
                (mtmdd::MtMddNode::NonTerminal(fnode), mtmdd::MtMddNode::Terminal(_)) => {
                    let tmp: Vec<_> = fnode
                        .iter()
                        .map(|f| vmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(fnode.header(), &tmp)
                }
                (mtmdd::MtMddNode::Terminal(_), mtmdd::MtMddNode::NonTerminal(gnode)) => {
                    let tmp: Vec<_> = gnode
                        .iter()
                        .map(|g| vmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(gnode.header(), &tmp)
                }
                (mtmdd::MtMddNode::NonTerminal(fnode), mtmdd::MtMddNode::NonTerminal(gnode))
                    if fnode.header().level() > gnode.header().level() =>
                {
                    vmdd_without(mdd, &fnode[0], &g, cache)
                }
                (mtmdd::MtMddNode::NonTerminal(fnode), mtmdd::MtMddNode::NonTerminal(gnode))
                    if fnode.header().level() < gnode.header().level() =>
                {
                    let tmp: Vec<_> = gnode
                        .iter()
                        .map(|g| vmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(gnode.header(), &tmp)
                }
                (mtmdd::MtMddNode::NonTerminal(fnode), mtmdd::MtMddNode::NonTerminal(gnode)) => {
                    let tmp: Vec<_> = fnode
                        .iter()
                        .zip(gnode.iter())
                        .map(|(f, g)| vmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(fnode.header(), &tmp)
                }
            };
            cache.insert(key, result.clone());
            result
        }
    }
}

fn bmdd_without(
    mdd: &mut mdd::Mdd,
    f: &mdd::MddNode,
    g: &mdd::MddNode, // minsol tree
    cache: &mut HashMap<(NodeId, NodeId), mdd::MddNode>,
) -> mdd::MddNode {
    let key = (f.id(), g.id());
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match (f, g) {
                (mdd::MddNode::Undet, _) => g.clone(),
                (_, mdd::MddNode::Undet) => mdd.undet(),
                (mdd::MddNode::Zero, mdd::MddNode::One) => mdd.one(),
                (mdd::MddNode::Zero, _) => g.clone(),
                (_, mdd::MddNode::Zero) => mdd.undet(), // probably this case is inpossible
                (mdd::MddNode::One, _) => mdd.undet(),
                (mdd::MddNode::NonTerminal(fnode), mdd::MddNode::One) => {
                    let tmp: Vec<_> = fnode
                        .iter()
                        .map(|f| bmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(fnode.header(), &tmp)
                }
                (mdd::MddNode::NonTerminal(fnode), mdd::MddNode::NonTerminal(gnode))
                    if fnode.header().level() > gnode.header().level() =>
                {
                    bmdd_without(mdd, &fnode[0], &g, cache)
                }
                (mdd::MddNode::NonTerminal(fnode), mdd::MddNode::NonTerminal(gnode))
                    if fnode.header().level() < gnode.header().level() =>
                {
                    let tmp: Vec<_> = gnode
                        .iter()
                        .map(|g| bmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(gnode.header(), &tmp)
                }
                (mdd::MddNode::NonTerminal(fnode), mdd::MddNode::NonTerminal(gnode)) => {
                    let tmp: Vec<_> = fnode
                        .iter()
                        .zip(gnode.iter())
                        .map(|(f, g)| bmdd_without(mdd, &f, &g, cache))
                        .collect();
                    mdd.create_node(fnode.header(), &tmp)
                }
            };
            cache.insert(key, result.clone());
            result
        }
    }
}

// pub fn mddextract(bdd: &mut bdd::Bdd, node: &bdd::BddNode) -> Vec<Vec<String>> {
//     let mut pathset = Vec::new();
//     _mddextract(node, &mut Vec::new(), &mut pathset);
//     pathset
// }

// fn _mddextract(node: &bdd::BddNode, path: &mut Vec<String>, pathset: &mut Vec<Vec<String>>) {
//     match node {
//         bdd::BddNode::Zero => (),
//         bdd::BddNode::One => pathset.push(path.clone()),
//         bdd::BddNode::NonTerminal(fnode) => {
//             let x = fnode.header().label();
//             path.push(x.to_string());
//             _extract(&fnode[1], path, pathset);
//             path.pop();
//             _extract(&fnode[0], path, pathset);
//         }
//     }
// }
