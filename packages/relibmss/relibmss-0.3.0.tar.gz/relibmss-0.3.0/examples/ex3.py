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
