# relibmss

A Python package for binary/multi state systems with BDD/MDD.

## Installation

```bash
pip install relibmss
```

## Usage

### Calculate the probability of a fault tree

```python
import relibmss as ms

# Create a fault tree (binary system)
ft = ms.FTree()

# Define events (This version only supports repeated events)
A = ft.defvar('A')
B = ft.defvar('B')
C = ft.defvar('C')

# Make a tree
top = A & B | C # & is AND gate, | is OR gate

# Set probabilities
prob = {
    'A': 0.1,
    'B': 0.2,
    'C': 0.3
}

# Calculate the probability
print(ft.prob(top, prob))

# Set the interval of the probability
prob = {
    'A': (0.1, 0.2),
    'B': (0.2, 0.3),
    'C': (0.3, 0.4)
}

# Calculate the probability
print(ft.prob_interval(top, prob))
```

### Obtain the minimal cut sets

```python
import relibmss as ms

# Create a fault tree (binary system)
ft = ms.FTree()

# Define events (This version only supports repeated events)
A = ft.defvar('A')
B = ft.defvar('B')
C = ft.defvar('C')

# Make a tree
top = ft.kofn(2, [A, B, C]) # k-of-n gate

# Obtain the minimal cut sets
s = ft.mcs(top) # s is a set of minimal cut sets (ZDD representation)

# Convert the ZDD representation to a list of sets
print(s.extract())
```

### Draw a BDD

```python
import relibmss as ms

# Create a binary decision diagram
ft = ms.FTree()

# Define variables
A = ft.defvar('A')
B = ft.defvar('B')
C = ft.defvar('C')

# Make a tree
top = A & B | C

# Draw the BDD
bdd = ft.getbdd(top)
source = bdd.dot() # source is a string of the dot language

# Example: Display the BDD in Jupyter Notebook
from graphviz import Source
from IPython.display import Image, display
Image(Source(source).pipe(format='png'))
```

### An example of a large fault tree

```python
## This is an example of a large fault tree
## Computational time may be long (about 1 minute)

import relibmss as ms

ft = ms.FTree()
c = [ft.defvar("c" + str(i)) for i in range(61)]

g62 = c[0] & c[1]
g63 = c[0] & c[2]
g64 = c[0] & c[3]
g65 = c[0] & c[4]
g66 = c[0] & c[5]
g67 = c[0] & c[6]
g68 = c[0] & c[7]
g69 = c[0] & c[8]
g70 = g62 | c[9]
g71 = g63 | c[10]
g72 = g64 | c[11]
g73 = g65 | c[12]
g74 = g62 | c[13]
g75 = g63 | c[14]
g76 = g64 | c[15]
g77 = g65 | c[16]
g78 = g62 | c[17]
g79 = g63 | c[18]
g80 = g64 | c[19]
g81 = g65 | c[20]
g82 = g62 | c[21]
g83 = g63 | c[22]
g84 = g64 | c[23]
g85 = g65 | c[24]
g86 = g62 | c[25]
g87 = g63 | c[26]
g88 = g64 | c[27]
g89 = g65 | c[28]
g90 = g66 | c[29]
g91 = g68 | c[30]
g92 = g67 | c[31]
g93 = g69 | c[32]
g94 = g66 | c[33]
g95 = g68 | c[34]
g96 = g67 | c[35]
g97 = g69 | c[36]
g98 = g66 | c[37]
g99 = g68 | c[38]
g100 = g67 | c[39]
g101 = g69 | c[40]
g102 = g66 | c[41]
g103 = g68 | c[42]
g104 = g67 | c[43]
g105 = g69 | c[44]
g106 = ft.kofn(3, [g70, g71, g72, g73])
g107 = ft.kofn(3, [g74, g75, g76, g77])
g108 = ft.kofn(3, [g78, g79, g80, g81])
g109 = ft.kofn(3, [g82, g83, g84, g85])
g110 = ft.kofn(3, [g86, g87, g88, g89])
g111 = ft.kofn(3, [g94, g95, g96, g97])
g112 = ft.kofn(3, [g98, g99, g100, g101])
g113 = g90 & g92
g114 = g91 & g93
g115 = g102 & g104
g116 = g103 & g105
g117 = g113 | c[45]
g118 = g114 | c[46]
g119 = g107 | g108 | c[51]
g120 = g109 | g110
g121 = g66 | g117 | c[47]
g122 = g68 | g118 | c[48]
g123 = g67 | g117 | c[49]
g124 = g69 | g118 | c[50]
g125 = ft.kofn(2, [g121, g123, g122, g124])
g126 = g111 | g112 | g125 | c[52]
g127 = g115 & g120
g128 = g116 & g120
g129 = g62 | g127 | c[53]
g130 = g63 | g128 | c[54]
g131 = g64 | g127 | c[55]
g132 = g65 | g128 | c[56]
g133 = g62 | g129 | c[57]
g134 = g63 | g130 | c[58]
g135 = g64 | g131 | c[59]
g136 = g65 | g132 | c[60]
g137 = ft.kofn(3, [g133, g134, g135, g136])
g138 = g106 | g119 | g137
g139 = g62 | g66 | g117 | g129 | c[47]
g140 = g63 | g68 | g118 | g130 | c[48]
g141 = g64 | g67 | g117 | g131 | c[49]
g142 = g65 | g69 | g118 | g132 | c[50]
g143 = g139 & g140 & g141 & g142
g144 = g111 | g112 | g143 | c[52]
top = g126 & g138 & g144

bdd = ft.getbdd(top)
print(bdd.count()) # The numbers of nodes and edges in the BDD

mcs = bdd.mcs() # Obtain the minimal cut sets from the BDD directly
print(mcs.extract())

prob = {
    'c0': 0.01,
    'c1': 0.051,
    'c2': 0.051,
    'c3': 0.051,
    'c4': 0.051,
    'c5': 0.112,
    'c6': 0.112,
    'c7': 0.112,
    'c8': 0.112,
    'c9': 0.016,
    'c10': 0.016,
    'c11': 0.016,
    'c12': 0.016,
    'c13': 0.0218,
    'c14': 0.0218,
    'c15': 0.0218,
    'c16': 0.0218,
    'c17': 0.015,
    'c18': 0.015,
    'c19': 0.015,
    'c20': 0.015,
    'c21': 0.016,
    'c22': 0.016,
    'c23': 0.016,
    'c24': 0.016,
    'c25': 0.015,
    'c26': 0.015,
    'c27': 0.015,
    'c28': 0.015,
    'c29': 0.0137,
    'c30': 0.0137,
    'c31': 0.0137,
    'c32': 0.0137,
    'c33': 0.016,
    'c34': 0.016,
    'c35': 0.016,
    'c36': 0.016,
    'c37': 0.016,
    'c38': 0.016,
    'c39': 0.016,
    'c40': 0.016,
    'c41': 0.0038,
    'c42': 0.0038,
    'c43': 0.0117,
    'c44': 0.0117,
    'c45': 0.00052,
    'c46': 0.00052,
    'c47': 0.018,
    'c48': 0.018,
    'c49': 0.018,
    'c50': 0.018,
    'c51': 0.000008,
    'c52': 0.000072,
    'c53': 0.015,
    'c54': 0.015,
    'c55': 0.015,
    'c56': 0.015,
    'c57': 0.0188,
    'c58': 0.0188,
    'c59': 0.0188,
    'c60': 0.0188
}

ft.prob(top, prob)

# Set the interval of the probability
error_lower = 0.5
error_upper = 1.5

prob = {
    'c0': (0.01 * error_lower, 0.01 * error_upper),
    'c1': (0.051 * error_lower, 0.051 * error_upper),
    'c2': (0.051 * error_lower, 0.051 * error_upper),
    'c3': (0.051 * error_lower, 0.051 * error_upper),
    'c4': (0.051 * error_lower, 0.051 * error_upper),
    'c5': (0.112 * error_lower, 0.112 * error_upper),
    'c6': (0.112 * error_lower, 0.112 * error_upper),
    'c7': (0.112 * error_lower, 0.112 * error_upper),
    'c8': (0.112 * error_lower, 0.112 * error_upper),
    'c9': (0.016 * error_lower, 0.016 * error_upper),
    'c10': (0.016 * error_lower, 0.016 * error_upper),
    'c11': (0.016 * error_lower, 0.016 * error_upper),
    'c12': (0.016 * error_lower, 0.016 * error_upper),
    'c13': (0.0218 * error_lower, 0.0218 * error_upper),
    'c14': (0.0218 * error_lower, 0.0218 * error_upper),
    'c15': (0.0218 * error_lower, 0.0218 * error_upper),
    'c16': (0.0218 * error_lower, 0.0218 * error_upper),
    'c17': (0.015 * error_lower, 0.015 * error_upper),
    'c18': (0.015 * error_lower, 0.015 * error_upper),
    'c19': (0.015 * error_lower, 0.015 * error_upper),
    'c20': (0.015 * error_lower, 0.015 * error_upper),
    'c21': (0.016 * error_lower, 0.016 * error_upper),
    'c22': (0.016 * error_lower, 0.016 * error_upper),
    'c23': (0.016 * error_lower, 0.016 * error_upper),
    'c24': (0.016 * error_lower, 0.016 * error_upper),
    'c25': (0.015 * error_lower, 0.015 * error_upper),
    'c26': (0.015 * error_lower, 0.015 * error_upper),
    'c27': (0.015 * error_lower, 0.015 * error_upper),
    'c28': (0.015 * error_lower, 0.015 * error_upper),
    'c29': (0.0137 * error_lower, 0.0137 * error_upper),
    'c30': (0.0137 * error_lower, 0.0137 * error_upper),
    'c31': (0.0137 * error_lower, 0.0137 * error_upper),
    'c32': (0.0137 * error_lower, 0.0137 * error_upper),
    'c33': (0.016 * error_lower, 0.016 * error_upper),
    'c34': (0.016 * error_lower, 0.016 * error_upper),
    'c35': (0.016 * error_lower, 0.016 * error_upper),
    'c36': (0.016 * error_lower, 0.016 * error_upper),
    'c37': (0.016 * error_lower, 0.016 * error_upper),
    'c38': (0.016 * error_lower, 0.016 * error_upper),
    'c39': (0.016 * error_lower, 0.016 * error_upper),
    'c40': (0.016 * error_lower, 0.016 * error_upper),
    'c41': (0.0038 * error_lower, 0.0038 * error_upper),
    'c42': (0.0038 * error_lower, 0.0038 * error_upper),
    'c43': (0.0117 * error_lower, 0.0117 * error_upper),
    'c44': (0.0117 * error_lower, 0.0117 * error_upper),
    'c45': (0.00052 * error_lower, 0.00052 * error_upper),
    'c46': (0.00052 * error_lower, 0.00052 * error_upper),
    'c47': (0.018 * error_lower, 0.018 * error_upper),
    'c48': (0.018 * error_lower, 0.018 * error_upper),
    'c49': (0.018 * error_lower, 0.018 * error_upper),
    'c50': (0.018 * error_lower, 0.018 * error_upper),
    'c51': (0.000008 * error_lower, 0.000008 * error_upper),
    'c52': (0.000072 * error_lower, 0.000072 * error_upper),
    'c53': (0.015 * error_lower, 0.015 * error_upper),
    'c54': (0.015 * error_lower, 0.015 * error_upper),
    'c55': (0.015 * error_lower, 0.015 * error_upper),
    'c56': (0.015 * error_lower, 0.015 * error_upper),
    'c57': (0.0188 * error_lower, 0.0188 * error_upper),
    'c58': (0.0188 * error_lower, 0.0188 * error_upper),
    'c59': (0.0188 * error_lower, 0.0188 * error_upper),
    'c60': (0.0188 * error_lower, 0.0188 * error_upper)
}

result = ft.prob_interval(top, prob)
print('lower: ', result.lower)
print('upper: ', result.upper)
```

### TODO for fault tree analysis

- FTA with MCS
- Importance analysis
- Sensitivity analysis
- Uncertainty analysis; etc.

## Multi-state system

### Definition of Gate

MSS does not have default gates. Users need to define gates by themselves. The operation that can be used in the definition of a gate is as follows:

- Arithmetic operations: `+`, `-`, `*`, `/`
- Comparison operations: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logical operations:
    - `mss.And`: AND gate
    - `mss.Or`: OR gate
    - `mss.Not`: NOT gate
    - `mss.switch`: Switch-case structure
    - `mss.case`: Case structure

```python
import relibmss as ms

# def for a gate with switch-case structure
def gate1(mss, x, y):
    return mss.switch([
        mss.case(cond=mss.And([x == 0, y == 0]), then=0),
        mss.case(cond=mss.Or([x == 0, y == 0]), then=1),
        mss.case(cond=mss.Or([x == 2, y == 2]), then=3),
        mss.case(cond=None, then=2) # default
    ])
```

### Example of a multi-state system

```python
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
```

### Draw an MDD

```python
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

mss = ms.MSS()

A = mss.defvar('A', 2)
B = mss.defvar('B', 3)
C = mss.defvar('C', 3)

# Define the order of variables
# this should be done before making MDD
mss.set_varorder({"A": 2, "B": 1, "C": 0})

sx = gate1(mss, B, C)
ss = gate2(mss, A, sx)

mdd = mss.getmdd(ss)
source = mdd.dot()

from graphviz import Source
from IPython.display import Image, display
Image(Source(source).pipe(format='png'))
```

### Obtain the minimal vector sets

```python
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

mss = ms.MSS()

A = mss.defvar('A', 2)
B = mss.defvar('B', 3)
C = mss.defvar('C', 3)

sx = gate1(mss, B, C)
ss = gate2(mss, A, sx)

mdd = mss.mvs(ss)
print(mdd.dot())
```

## TODO

- Add more examples
- Add more functions for fault tree analysis
- Add more functions for multi-state system analysis

## License

MIT License

