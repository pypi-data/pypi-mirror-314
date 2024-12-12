import relibmss as ms

# Create a binary decision diagram
bss = ms.BSS()

# Define variables
A = bss.defvar('A')
B = bss.defvar('B')
C = bss.defvar('C')

# Make a tree
top = A & B | C

# Draw the BDD
bdd = bss.getbdd(top)
source = bdd.dot() # source is a string of the dot language
print(source)

# Example: Display the BDD in Jupyter Notebook
from graphviz import Source
from IPython.display import Image, display
Image(Source(source).pipe(format='png'))
