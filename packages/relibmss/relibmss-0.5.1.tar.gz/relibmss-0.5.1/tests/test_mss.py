import relibmss as ms

def test_mss():
    ctx = ms.MSS()
    x = ctx.defvar("x", 2)
    y = ctx.defvar("y", 3)
    z = ctx.defvar("z", 3)
    v = x * y + z
    v = ctx.And([x >= 1, y <= 1, z == 0])
    print(v)

    tree = ctx.mdd.rpn("x 1 >= y 1 <= &&", ctx.vars)
    tree2 = ctx.getmdd(v)

    print(tree.dot())
    print(tree2.dot())

def test_mss3():
    mss = ms.MSS()
    x = mss.defvar("x", 3)
    y = mss.defvar("y", 3)
    z = mss.defvar("z", 3)
    s1 = mss.ifelse(x + y == z, 100, 200)
    print(s1)
    tree = mss.getmdd(s1)
    print(tree.dot())

def test_mdd():
    mdd = ms.MDD()
    x = mdd.defvar("x", 3)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    # tree = mdd.rpn("x y + z == 100 200 ?", {})
    # print(tree.dot())

def test_bdd1():
    bdd = ms.BDD()
    x = bdd.defvar("x")
    y = bdd.defvar("y")
    z = bdd.defvar("z")
    v = x & y | z
    print(v)
    print(v.dot())

def test_mdd2():
    mdd = ms.MDD()
    x = mdd.defvar("x", 3)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    v = x + y == z + 1
    print(v.dot())
    v2 = mdd.ifelse(x + y == z, 100, 200)
    print(v2.dot())
    v3 = mdd.ifelse(mdd.And([x + y == z, x == z]), 100, 200)
    print(v3.dot())

def test_mdd3():
    mdd = ms.MDD()
    x = mdd.defvar("x", 3)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    v = mdd.ifelse(x + y == z, 100, 200)
    print(v.dot())

def test_mdd4():
    mdd = ms.MDD()
    x = mdd.defvar("x", 3)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    v = mdd.ifelse(mdd.And([x + y == z, x == z]), 100, 200)
    print(v.dot())

def test_mdd5():
    mdd = ms.MDD()
    x = mdd.defvar("x", 3)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    v = mdd.ifelse(mdd.Or([x + y == z, x == z]), 100, 200)
    print(v.dot())

def test_mdd5():
    mdd = ms.MDD()
    x = mdd.defvar("x", 10)
    y = mdd.defvar("y", 3)
    z = mdd.defvar("z", 3)
    v = mdd.ifelse(mdd.Not(mdd.Or([x + y == z, x == z])), 100, 200)
    print(v.dot())

def test_mss6():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)

    def gate1(x, y):
        return ctx.ifelse(
            ctx.And([x == 0, y == 0]), 0,
            ctx.ifelse(
                ctx.Or([x == 0, y == 0]), 1,
                    ctx.ifelse(
                        ctx.Or([x == 2, y == 2]), 3,
                    2
                )
            )
        )
    
    def gate2(x, y):
        return ctx.ifelse(x == 0, 0, y)

    ctx.mdd.defvar("C", 3)
    ctx.mdd.defvar("B", 3)
    ctx.mdd.defvar("A", 2)

    sx = gate1(B, C)
    ss = gate2(A, sx)

    print(ss)
    mdd = ctx.getmdd(ss)
    print(mdd.dot())

def test_mss7():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)

    x = ctx.switch([
        ctx.case(cond=ctx.And([A == 0, B == 0]), then=0),
        ctx.case(cond=ctx.Or([A == 0, B == 0]), then=1),
        ctx.case(cond=None, then=2)
    ])

    print(x)

def test_mss8():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)
    ctx.set_varorder({"A": 2, "B": 1, "C": 0}) # this should be done before making MDD

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    print(ss)
    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    print(mdd.dot())

def test_mss9():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)
    ctx.set_varorder({"A": 2, "B": 1, "C": 0}) # this should be done before making MDD

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    prob = {
        "A": [0.9, 0.1],
        "B": [0.5, 0.2, 0.3],
        "C": [0.2, 0.3, 0.5]
    }

    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    print(ctx.prob(ss, prob))

def test_mss10():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)
    ctx.set_varorder({"A": 2, "B": 1, "C": 0}) # this should be done before making MDD

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    prob = {
        "A": [(0.9, 0.91), (0.09, 0.1)],
        "B": [(0.5, 0.51), (0.2, 0.21), (0.28, 0.3)],
        "C": [(0.2, 0.21), (0.3, 0.31), (0.5, 0.51)]
    }

    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    print(ctx.prob_interval(ss, prob))

def test_mss11():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)
    ctx.set_varorder({"A": 2, "B": 1, "C": 0}) # this should be done before making MDD

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    v = mdd.mpvs()
    print(v.dot())

def test_mss12():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    v = mdd.mpvs()
    print(v.dot())

def test_mss13():
    def gate1(ctx, x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    # def gate2(ctx, x, y):
    #     return ctx.switch([
    #         ctx.case(cond=x == 0, then=0),
    #         ctx.case(cond=None, then=y)
    #     ])

    ctx = ms.MSS()
    x = ctx.defvar("x", 3)
    y = ctx.defvar("y", 3)
    xdash = ctx.defvar("xdash", 3)
    ydash = ctx.defvar("ydash", 3)

    # gate1 is the increasing function or not?
    ss = ctx.ifelse(ctx.And([x <= xdash, y <= ydash]), gate1(ctx, x, y) <= gate1(ctx, xdash, ydash), True)
    print(ss)

    v = ctx.getmdd(ss)
    print(v.dot())

def test_mss13():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then=0),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=1),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=3),
            ctx.case(cond=None, then=2)
        ])

    def gate2(x, y):
        return ctx.switch([
            ctx.case(cond=x == 0, then=0),
            ctx.case(cond=None, then=y)
        ])    

    sx = gate1(B, C)
    ss = gate2(A, sx)

    mdd = ctx.getmdd(ss) # this is the time when MDD is created
    v = mdd.mpvs()
    print(v.dot())

def test_mss14():
    ctx = ms.MSS()
    A = ctx.defvar("A", 2)
    B = ctx.defvar("B", 3)
    C = ctx.defvar("C", 3)

    def gate1(x, y):
        return ctx.switch([
            ctx.case(cond=ctx.And([x == 0, y == 0]), then= x == y),
            ctx.case(cond=ctx.Or([x == 0, y == 0]), then=x != y),
            ctx.case(cond=ctx.Or([x == 2, y == 2]), then=x <= y),
            ctx.case(cond=None, then=False)
        ])

    sx = gate1(B, C)

    mdd = ctx.getmdd(sx)
    v = mdd.mpvs()
    print(v.dot())

    prob = {
        "B": [0.5, 0.5, 0.0],
        "C": [0.5, 0.2, 0.3]
    }

    print(ctx.prob(sx, prob))
