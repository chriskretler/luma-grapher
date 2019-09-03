import numpy as np
import numpy.polynomial.polynomial as poly
import sys

# This function leverages numpy polynomial functions to create an estimate of the input.
# This could be used as input to remedy situations where we identify overshoot, assuming
# polynomial functions do not estimate the overshoot. They will be more accurate
# if we feed them portions of a line, instead of the whole line.
def find_fit(y):
   x = np.zeros_like(y)
   for i in range(0, len(x)):
      x[i] = i
      
   # https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html
   coefs = np.polyfit(x, y, 2)
   
   # https://docs.scipy.org/doc/numpy/reference/generated/numpy.poly1d.html
   print np.poly1d(coefs)


file = sys.argv[1]

with open(file) as f:
   array = np.array(map(int, f))

find_fit(array)