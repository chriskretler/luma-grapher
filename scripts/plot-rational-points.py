#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt

if len(sys.argv) < 2:
   print("function signature: plot-rational-points.py input-file rational-points-file")
   exit()

file = sys.argv[1]

with open(file) as f:
   array = list(map(int, f.readlines()))

# Plot input variable as primary graph.
plt.plot(array)

# Also plot list of points of identified overshoot.
rational_array = genfromtxt(sys.argv[2], delimiter=',')

# First variable is x coordinate, second is original luma value.
plt.plot(rational_array[:,0], rational_array[:,1], 'o')

# adjust axis, first two vals are x, second two are y.
plt.axis([0, len(array)-1, 0, 255])

# Sample Legend
plt.ylabel('Luma Values')

plt.show()
