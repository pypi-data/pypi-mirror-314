import relibmss as ms

# Define gates
def gate1(mss, x, y):
    return mss.switch([
        mss.case(cond=mss.And([x == 0, y == 0]), then=0),
        mss.case(cond=mss.Or([x == 0, y == 0]), then=1),
        mss.case(cond=mss.Or([x == 2, y == 2]), then=3),
        mss.case(cond=None, then=2) # default
    ])

def gate2(mss, x, y):
    return mss.switch([
        mss.case(cond=x == 0, then=0),
        mss.case(cond=None, then=y)
    ])

mss = ms.MSS() # Context for the multi-state system

# Define variables

A = mss.defvar('A', 2) # 2 states
B = mss.defvar('B', 3) # 3 states
C = mss.defvar('C', 3) # 3 states

# Define a multi-state system
sx = gate1(mss, B, C)
ss = gate2(mss, A, sx)

# Define probabilities
prob = {
    'A': [0.1, 0.9],
    'B': [0.2, 0.3, 0.5],
    'C': [0.3, 0.4, 0.3]
}

# Calculate the probability
print(mss.prob(ss, prob))
