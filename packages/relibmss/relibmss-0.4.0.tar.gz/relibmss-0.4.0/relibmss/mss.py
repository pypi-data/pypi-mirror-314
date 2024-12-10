import relibmss as ms

class _Expression:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('+')))
    
    def __sub__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('-')))
    
    def __mul__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('*')))
    
    def __truediv__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('/')))
    
    def __eq__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('==')))
    
    def __ne__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('!=')))
    
    def __lt__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('<')))
    
    def __le__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('<=')))
    
    def __gt__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('>')))
    
    def __ge__(self, other):
        if not isinstance(other, _Expression):
            other = _Expression(other)
        return _Expression((self, other, _Expression('>=')))
    
    def __str__(self):
        if isinstance(self.value, tuple):
            return ' '.join([x.to_rpn() for x in self.value])
        return str(self.value)

    def to_rpn(self):
        if isinstance(self.value, tuple):
            return ' '.join([x.to_rpn() for x in self.value])
        return str(self.value)

class _Case:
    def __init__(self, cond, then):
        self.cond = cond
        self.then = then

class Context:
    def __init__(self):
        self.vars = {}
        self.mdd = ms.MddMgr()

    def defvar(self, name, domain):
        self.vars[name] = domain
        return _Expression(name)
    
    def set_varorder(self, x: dict):
        for varname in sorted(x, key=x.get):
            self.mdd.defvar(varname, self.vars[varname])
    
    def __str__(self):
        return str(self.vars)
    
    def getmdd(self, arg: _Expression):
        if not isinstance(arg, _Expression):
            arg = _Expression(arg)
        rpn = arg.to_rpn()
        return self.mdd.rpn(rpn, self.vars)

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
            x = _Expression((x, y, _Expression('&&')))
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
            x = _Expression((x, y, _Expression('||')))
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
    
    def case(self, then, cond = None):
        if not isinstance(cond, _Expression):
            cond = _Expression(cond)
        if not isinstance(then, _Expression):
            then = _Expression(then)
        return _Case(cond=cond, then=then)
    
    def switch(self, conds: list):
        assert len(conds) >= 2
        if len(conds) == 2:
            assert isinstance(conds[0], _Case) and isinstance(conds[1], _Case)
            return self.ifelse(conds[0].cond, conds[0].then, conds[1].then)
        else:
            x = conds[0]
            if not isinstance(x, _Case):
                raise ValueError("The element must be a Case object")
            return self.ifelse(x.cond, x.then, self.switch(conds[1:]))

    def prob(self, arg: _Expression, values: dict):
        top = self.getmdd(arg)
        return top.prob(values)
        
    def prob_interval(self, arg: _Expression, values: dict):
        values = {k: [ms.Interval(u[0], u[1]) for u in v] for k, v in values.items()}
        top = self.getmdd(arg)
        return top.prob_interval(values)
    
    def mvs(self, arg: _Expression):
        top = self.getmdd(arg)
        return top.mvs()



