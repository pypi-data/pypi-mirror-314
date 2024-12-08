import relibmss as ms

def test_ft1():
    ctx = ms.FTree()
    x = ctx.defvar("x")
    y = ctx.defvar("y")
    z = ctx.defvar("z")
    v = x & y | z
    u = ctx.kofn(2, [x, y, z])
    print(u)
    print(ctx.getbdd(u).dot())

def test_mss():
    ctx = ms.MSS()
    x = ctx.defvar("x", range(2))
    y = ctx.defvar("y", range(3))
    z = ctx.defvar("z", range(3))
    v = x * y + z
    v = ctx.And([x >= 1, y <= 1, z == 0])
    print(v)

    tree = ctx.mdd.rpn("x 1 >= y 1 <= &&", ctx.vars)
    tree2 = ctx.getmdd(v)

    print(tree.dot())
    print(tree2.dot())

def test_mss3():
    mss = ms.MSS()
    x = mss.defvar("x", range(3))
    y = mss.defvar("y", range(3))
    z = mss.defvar("z", range(3))
    s1 = mss.IfThenElse(x + y == z, 100, 200)
    print(s1)
    tree = mss.getmdd(s1)
    print(tree.dot())

def test_mdd():
    mdd = ms.MDD()
    x = mdd.defvar("x", range(3))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
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
    x = mdd.defvar("x", range(3))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
    v = x + y == z + 1
    print(v.dot())
    v2 = mdd.IfThenElse(x + y == z, 100, 200)
    print(v2.dot())
    v3 = mdd.IfThenElse(mdd.And([x + y == z, x == z]), 100, 200)
    print(v3.dot())

def test_mdd3():
    mdd = ms.MDD()
    x = mdd.defvar("x", range(3))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
    v = mdd.IfThenElse(x + y == z, 100, 200)
    print(v.dot())

def test_mdd4():
    mdd = ms.MDD()
    x = mdd.defvar("x", range(3))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
    v = mdd.IfThenElse(mdd.And([x + y == z, x == z]), 100, 200)
    print(v.dot())

def test_mdd5():
    mdd = ms.MDD()
    x = mdd.defvar("x", range(3))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
    v = mdd.IfThenElse(mdd.Or([x + y == z, x == z]), 100, 200)
    print(v.dot())

def test_mdd5():
    mdd = ms.MDD()
    x = mdd.defvar("x", range(10))
    y = mdd.defvar("y", range(3))
    z = mdd.defvar("z", range(3))
    v = mdd.IfThenElse(mdd.Not(mdd.Or([x + y == z, x == z])), 100, 200)
    print(v.dot())

def test_ft3():
    ctx = ms.FTree()
    x = ctx.defvar("x")
    y = ctx.defvar("y")
    z = ctx.defvar("z")
    u = ctx.kofn(2, [x, y, z])
    print(u)
    print(ctx.getbdd(u).dot())
    print("prob:", ctx.prob(u, {"x": 0.3, "y": 0.2, "z": 0.1}))
    m = ctx.mcs(u)
    print(m.extract())

def test_interval4():
    x = ms.Interval(0, 1)
    print(x)

def test_interval5():
    ctx = ms.FTree()
    x = ctx.defvar("x")
    y = ctx.defvar("y")
    z = ctx.defvar("z")
    u = ctx.kofn(2, [x, y, z])
    print(u)
    print(ctx.getbdd(u).dot())
    problist = {
        "x": (1.0e-3, 1.0e-2),
        "y": (1.0e-4, 1.0e-3),
        "z": (1.0e-3, 1.0e-2)
    }
    print("prob:", ctx.prob_interval(u, problist))
