import numpy as np
from datetime import datetime

time1 = datetime.now()

with open('Sather-line-352-original.txt') as f:
   array = np.array(map(int, f))

def find_diff(array, spacing, limit):
   return ret_high_values(array, np.diff(array, spacing), limit)

def find_gradient(array, spacing, limit):
   return ret_high_values(array, np.gradient(array, spacing), limit)

# returns the x position of places where
# the gradient is above a certain value.
def ret_high_values(array, grad_array, limit):
   x_pos_array = []
   for it in range(len(grad_array)):
      if abs(grad_array[it]) > limit: 
         x_pos_array_row = []
         x_pos_array_row.append(it)
         x_pos_array_row.append(array[it])
         x_pos_array.append(x_pos_array_row)
   return x_pos_array

overshoot_points = find_diff(array, 1, 12)
#overshoot_points = find_gradient(array, 5, 2.5)
np.savetxt("./overshoot_points.txt", overshoot_points, fmt='%i, %i', delimiter=",", newline="\n")

time2 = datetime.now()
print (time2 - time1)
