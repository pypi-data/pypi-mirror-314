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
