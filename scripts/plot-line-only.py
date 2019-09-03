#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt

file = sys.argv[1]

with open(file) as f:
   array = map(int, f)

# Plot input variable as primary graph.
plt.plot(array)

# adjust axis, first two vals are x, second two are y.
plt.axis([0, len(array)-1, 0, 255])

# Sample Legend
plt.ylabel('Luma Values')

plt.show()
