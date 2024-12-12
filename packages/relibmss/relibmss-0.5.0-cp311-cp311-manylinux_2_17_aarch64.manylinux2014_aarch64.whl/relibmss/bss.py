import relibmss as ms

def _to_rpn(expr):
    stack = [expr]
    rpn = []
    while len(stack) > 0:
        node = stack.pop()
        if isinstance(node.value, tuple):
            for i in range(len(node.value) - 1, -1, -1):
                stack.append(node.value[i])
        else:
            rpn.append(str(node.value))
    return ' '.join(rpn)

class _Expression:
    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('&')))
    
    def __or__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('|')))

    def __str__(self):
        if isinstance(self.value, tuple):
            return _to_rpn(self)
        return str(self.value)

    def _to_rpn(self):
        if isinstance(self.value, tuple):
            return _to_rpn(self)
        return str(self.value)

class Context:
    def __init__(self):
        self.vars = set([])
        self.bdd = ms.BDD()

    def defvar(self, name):
        self.vars.add(name)
        return _Expression(name)
    
    def set_varorder(self, x: list):
        for varname in x:
            self.bdd.defvar(varname)

    def __str__(self):
        return str(self.vars)
    
    def getbdd(self, arg: _Expression):
        if not isinstance(arg, _Expression):
            arg = _Expression(arg)
        rpn = arg._to_rpn()
        return self.bdd.rpn(rpn, self.vars)
    
    def const(self, value):
        return _Expression(value)

    def And(self, args: list):
        assert len(args) > 0
        if not isinstance(args[0], _Expression):
            args[0] = _Expression(args[0])
        if len(args) == 1:
            return args[0]
        x = args[0]
        for y in args[1:]:
            if not isinstance(y, _Expression):
                y = _Expression(y)
            x = _Expression((x, y, _Expression('&')))
        return x

    def Or(self, args: list):
        assert len(args) > 0
        if not isinstance(args[0], _Expression):
            args[0] = _Expression(args[0])
        if len(args) == 1:
            return args[0]
        x = args[0]
        for y in args[1:]:
            if not isinstance(y, _Expression):
                y = _Expression(y)
            x = _Expression((x, y, _Expression('|')))
        return x

    def Not(self, arg: _Expression):
        if not isinstance(arg, _Expression):
            arg = _Expression(arg)
        return _Expression((arg, _Expression('!')))

    def ifelse(self, condition: _Expression, then_expr: _Expression, else_expr: _Expression):
        if not isinstance(condition, _Expression):
            condition = _Expression(condition)
        if not isinstance(then_expr, _Expression):
            then_expr = _Expression(then_expr)
        if not isinstance(else_expr, _Expression):
            else_expr = _Expression(else_expr)
        return _Expression((condition, then_expr, else_expr, _Expression('?')))

    def kofn(self, k: int, args: list):
        assert k <= len(args)
        if k == 1:
            return self.Or(args)
        elif k == len(args):
            return self.And(args)
        else:
            return self.ifelse(args[0], self.kofn(k-1, args[1:]), self.kofn(k, args[1:]))

    def prob(self, arg: _Expression, values: dict):
        top = self.getbdd(arg)
        return top.prob(values)
    
    def prob_interval(self, arg: _Expression, values: dict):
        values = {k: ms.Interval(v[0], v[1]) for k, v in values.items()}
        top = self.getbdd(arg)
        return top.prob_interval(values)

    def mpvs(self, arg: _Expression):
        top = self.getbdd(arg)
        return top.mpvs()

