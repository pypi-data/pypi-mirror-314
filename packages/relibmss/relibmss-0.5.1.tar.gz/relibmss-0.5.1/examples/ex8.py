import relibmss as ms
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def dist(self, p):
        return np.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

np.random.seed(1234)

bss = ms.BSS()
m = 100
n = 100
ps = {'p'+str(i): Point(np.random.rand(), np.random.rand()) for i in range(m)}
vars = {'p'+str(i): bss.defvar('p'+str(i)) for i in range(m)}
# sort ps based on the distance from (0,0)
sortedps = [k for (k,v) in sorted(ps.items(), key=lambda x: x[1].dist(Point(0,0)))]
print(sortedps)
bss.set_varorder(sortedps)

grid = {'grid_{}_{}'.format(i,j): Point(x,y) for (i,x) in enumerate(np.linspace(0,1,n)) for (j,y) in enumerate(np.linspace(0,1,n))}

r = 0.2
result = []
for (k,v) in grid.items():
    nm = [pn for (pn, pv) in ps.items() if pv.dist(v) <= r]
    tmp = bss.const(False)
    for x in nm:
        tmp = vars[x] | tmp
    result.append(tmp)

expr = bss.const(True)
for x in result:
    expr = x & expr

# print(str(expr))

bdd = bss.getbdd(expr)
print(bdd.size())

# mpvs = bdd.mpvs()
# print(mpvs.count_set())

prob = {'p'+str(i): 0.9 for i in range(m)}

print(bdd.prob(prob))
