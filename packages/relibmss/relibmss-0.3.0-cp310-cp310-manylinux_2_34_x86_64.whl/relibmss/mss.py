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

class Context:
    def __init__(self):
        self.vars = {}
        self.mdd = ms.MddMgr()

    def defvar(self, name, domain):
        self.vars[name] = domain
        return _Expression(name)
    
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

    def IfThenElse(self, condition: _Expression, then_expr: _Expression, else_expr: _Expression):
        if not isinstance(condition, _Expression):
            condition = _Expression(condition)
        if not isinstance(then_expr, _Expression):
            then_expr = _Expression(then_expr)
        if not isinstance(else_expr, _Expression):
            else_expr = _Expression(else_expr)
        return _Expression((condition, then_expr, else_expr, _Expression('?')))

