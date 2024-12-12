import relibmss as ms

def test_ft1():
    ctx = ms.BSS()
    x = ctx.defvar("x")
    y = ctx.defvar("y")
    z = ctx.defvar("z")
    v = x & y | z
    u = ctx.kofn(2, [x, y, z])
    print(u)
    print(ctx.getbdd(u).dot())

def test_bdd1():
    bdd = ms.BDD()
    x = bdd.defvar("x")
    y = bdd.defvar("y")
    z = bdd.defvar("z")
    v = x & y | z
    print(v)
    print(v.dot())

def test_ft3():
    ctx = ms.BSS()
    x = ctx.defvar("x")
    y = ctx.defvar("y")
    z = ctx.defvar("z")
    u = ctx.kofn(2, [x, y, z])
    print(u)
    print(ctx.getbdd(u).dot())
    print("prob:", ctx.prob(u, {"x": 0.3, "y": 0.2, "z": 0.1}))
    m = ctx.mpvs(u)
    print('mcs: ', m.extract())

def test_interval4():
    x = ms.Interval(0, 1)
    print(x)

def test_interval5():
    ctx = ms.BSS()
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

