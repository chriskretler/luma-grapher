import matplotlib.pyplot as plt
import sys

file = sys.argv[1]

with open(file) as f:
   array = map(int, f)

# develop basic plot
plt.plot(array)

# adjust axis, first two vals are x, second two are y.
plt.axis([0, len(array)-1, 0, 255])

# sample legend
plt.ylabel('Luma Values')

# display
plt.show()
