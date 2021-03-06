#!/usr/bin/env python
import sys
import matplotlib.pyplot as plt
from numpy import genfromtxt

file = sys.argv[1]

with open(file) as f:
   array = map(int, f)

# Plot input variable as primary graph.
plt.plot(array)

# Also plot list of points of identified overshoot.
overshoot_array = genfromtxt('overshoot_points.txt', delimiter=',')

# First variable is x coordinate, second is original luma value.
plt.plot(overshoot_array[:,0], overshoot_array[:,1], 'o')

# adjust axis, first two vals are x, second two are y.
plt.axis([0, len(array)-1, 0, 255])

# Sample Legend
plt.ylabel('Luma Values')

plt.show()
