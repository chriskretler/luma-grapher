import numpy as np
import numpy.polynomial.polynomial as poly
from datetime import datetime
import sys

time1 = datetime.now()

file = sys.argv[1]

with open(file) as f:
   array = np.array(map(int, f))

def find_fit(y):
   x = np.zeros_like(y)
   for i in range(0, len(x)):
      x[i] = i
   coefs = np.polyfit(x, y, 2)
   print np.poly1d(coefs)

find_fit(array)

#overshoot_points = find_gradient(array, 5, 2.5)
#print overshoot_points
#np.savetxt("./overshoot_points.txt", overshoot_points, fmt='%i, %i', delimiter=",", newline="\n")

time2 = datetime.now()
print (time2 - time1)
