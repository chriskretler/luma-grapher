import numpy as np
from datetime import datetime
import operator
import sys

time1 = datetime.now()

file = sys.argv[1]

with open(file) as f:
   array = np.array(map(int, f))

# returns x position where average diff across spacing > limit.
def find_diff(array, spacing, limit):
   return ret_max_min_values(array, np.diff(array, spacing), limit)

# returns x position where gradient > limit.
def find_gradient(array, spacing, limit):
   return ret_max_min_values(array, np.gradient(array, spacing), limit)

# returns x position where gradient > limit.
def ret_max_min_values(array, grad_array, limit):
   x_pos_array = []
   arr_range = 6
   for it in range(len(grad_array)):
      if abs(grad_array[it]) > limit:
      #if grad_array[it] < limit:  
         # for each value, construct temp array and return
         # both the max and min coordinates and values.
         temp_array = array[it-arr_range:it+arr_range+1]

         # construct a list of the minimum index and minimum
         # value from a range around a high gradient array
         x_pos_array_row = []
         min_index, min_value = min(enumerate(temp_array), key=operator.itemgetter(1))
         min_index = it - arr_range + min_index
         x_pos_array_row.append(min_index)
         x_pos_array_row.append(min_value)
         x_pos_array.append(x_pos_array_row)

         # and do the same for maximums
         x_pos_array_row = []
         max_index, max_value = max(enumerate(temp_array), key=operator.itemgetter(1))
         max_index = it - arr_range + max_index
         x_pos_array_row.append(max_index)
         x_pos_array_row.append(max_value)
         x_pos_array.append(x_pos_array_row)
   return x_pos_array

overshoot_points = find_diff(array, spacing=1, limit=15)
#overshoot_points = find_gradient(array, 5, 2.5)
#print ret_idx(array)
#print overshoot_points
np.savetxt("./overshoot_points.txt", overshoot_points, fmt='%i, %i', delimiter=",", newline="\n")

time2 = datetime.now()
print (time2 - time1)
