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
