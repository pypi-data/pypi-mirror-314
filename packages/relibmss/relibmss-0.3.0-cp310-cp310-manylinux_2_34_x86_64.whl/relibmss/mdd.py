import relibmss as ms

class _Expression:
    def __init__(self, node):
        self.node = node

    def __add__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.add(other.node))
    
    def __radd__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.add(other.node))

    def __sub__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.sub(other.node))
    
    def __rsub__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.sub(other.node))
    
    def __mul__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.mul(other.node))
    
    def __rmul__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.mul(other.node))

    def __truediv__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.div(other.node))

    def __eq__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.eq(other.node))

    def __ne__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.ne(other.node))

    def __lt__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.lt(other.node))

    def __le__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.le(other.node))

    def __gt__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.gt(other.node))

    def __ge__(self, other):
        if isinstance(other, int):
            other = _Expression(self.node.value(other))
        elif isinstance(other, bool):
            other = _Expression(self.node.boolean(other))
        return _Expression(self.node.ge(other.node))    
    
    def dot(self):
        return self.node.dot()

class MDD:
    def __init__(self):
        self.mddmgr = ms.MddMgr()

    def defvar(self, name, domain):
        return _Expression(self.mddmgr.defvar(name, domain))
    
    def to_expr(self, x):
        if isinstance(x, int):
            return _Expression(self.mddmgr.val(x))
        elif isinstance(x, bool):
            if x:
                return _Expression(self.mddmgr.one())
            else:
                return _Expression(self.mddmgr.zero())
        return x
    
    def And(self, args):
        exprs = [self.to_expr(arg) for arg in args]
        nodes = [expr.node for expr in exprs]
        return _Expression(self.mddmgr._and(nodes))
    
    def Or(self, args):
        exprs = [self.to_expr(arg) for arg in args]
        nodes = [expr.node for expr in exprs]
        return _Expression(self.mddmgr._or(nodes))
    
    def Not(self, arg):
        expr = self.to_expr(arg)
        return _Expression(self.mddmgr._not(expr.node))
    
    def IfThenElse(self, condition, then_expr, else_expr):
        condition = self.to_expr(condition)
        then_expr = self.to_expr(then_expr)
        else_expr = self.to_expr(else_expr)
        return _Expression(self.mddmgr.ifelse(condition.node, then_expr.node, else_expr.node))

