// mod ft

use std::collections::HashMap;
use std::ops::{Add, Mul, Sub};

use dd::bdd;
use dd::common::NodeId;
use dd::nodes::NonTerminal;

pub fn prob<T>(
    bdd: &mut bdd::Bdd,
    node: &bdd::BddNode,
    pv: &HashMap<String, T>,
    cache: &mut HashMap<NodeId, T>,
) -> T
where
    T: Add<Output = T> + Sub<Output = T> + Mul<Output = T> + Clone + Copy + PartialEq + From<f64>,
{
    let key = node.id();
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                bdd::BddNode::Zero => T::from(1.0),
                bdd::BddNode::One => T::from(0.0),
                bdd::BddNode::NonTerminal(fnode) => {
                    let x = fnode.header().label();
                    let fp = *pv.get(x).unwrap_or(&T::from(0.0));
                    let low = prob(bdd, &fnode[0], pv, cache);
                    let high = prob(bdd, &fnode[1], pv, cache);
                    fp * low + (T::from(1.0) - fp) * high
                }
            };
            cache.insert(key, result);
            result
        }
    }
}

pub fn minsol(
    dd: &mut bdd::Bdd,
    node: &bdd::BddNode,
    cache1: &mut HashMap<NodeId, bdd::BddNode>,
    cache2: &mut HashMap<(NodeId, NodeId), bdd::BddNode>,
) -> bdd::BddNode {
    let key = node.id();
    match cache1.get(&key) {
        Some(x) => x.clone(),
        None => {
            let result = match node {
                bdd::BddNode::Zero => dd.zero(),
                bdd::BddNode::One => dd.one(),
                bdd::BddNode::NonTerminal(fnode) => {
                    let tmp = minsol(dd, &fnode[1], cache1, cache2);
                    let high = bdd_without(dd, &tmp, &fnode[0], cache2);
                    let low = minsol(dd, &fnode[0], cache1, cache2);
                    dd.create_node(fnode.header(), &low, &high)
                }
            };
            cache1.insert(key, result.clone());
            result
        }
    }
}

pub fn bdd_without(
    dd: &mut bdd::Bdd,
    f: &bdd::BddNode, // minsol tree
    g: &bdd::BddNode,
    cache: &mut HashMap<(NodeId, NodeId), bdd::BddNode>,
) -> bdd::BddNode {
    let key = (f.id(), g.id());
    match cache.get(&key) {
        Some(x) => x.clone(),
        None => {
            let node = match (f, g) {
                (bdd::BddNode::Zero, _) => dd.zero(),
                (_, bdd::BddNode::Zero) => f.clone(),
                (_, bdd::BddNode::One) => dd.zero(),
                (bdd::BddNode::One, bdd::BddNode::Zero) => dd.one(),
                (bdd::BddNode::One, bdd::BddNode::NonTerminal(gnode)) => {
                    let low = bdd_without(dd, f, &gnode[0], cache);
                    let high = bdd_without(dd, f, &gnode[1], cache);
                    dd.create_node(gnode.header(), &low, &high)
                },
                (bdd::BddNode::NonTerminal(fnode), bdd::BddNode::NonTerminal(gnode))
                    if fnode.id() == gnode.id() =>
                {
                    dd.zero()
                }
                (bdd::BddNode::NonTerminal(fnode), bdd::BddNode::NonTerminal(gnode))
                    if fnode.level() > gnode.level() =>
                {
                    let low = bdd_without(dd, &fnode[0], g, cache);
                    let high = bdd_without(dd, &fnode[1], g, cache);
                    dd.create_node(fnode.header(), &low, &high)
                }
                (bdd::BddNode::NonTerminal(fnode), bdd::BddNode::NonTerminal(gnode))
                    if fnode.level() < gnode.level() =>
                {
                    bdd_without(dd, f, &gnode[0], cache)
                }
                (bdd::BddNode::NonTerminal(fnode), bdd::BddNode::NonTerminal(gnode)) => {
                    let low = bdd_without(dd, &fnode[0], &gnode[0], cache);
                    let high = bdd_without(dd, &fnode[1], &gnode[1], cache);
                    dd.create_node(fnode.header(), &low, &high)
                }
            };
            cache.insert(key, node.clone());
            node
        }
    }
}

pub fn extract(node: &bdd::BddNode, path: &mut Vec<String>, pathset: &mut Vec<Vec<String>>) {
    match node {
        bdd::BddNode::Zero => (),
        bdd::BddNode::One => pathset.push(path.clone()),
        bdd::BddNode::NonTerminal(fnode) => {
            let x = fnode.header().label();
            path.push(x.to_string());
            extract(&fnode[1], path, pathset);
            path.pop();
            extract(&fnode[0], path, pathset);
        }
    }
}
