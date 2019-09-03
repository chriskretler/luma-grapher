import numpy as np
import operator
import sys

# returns x position where average diff across spacing > limit.
def find_diff(input, limit):
   # https://docs.scipy.org/doc/numpy/reference/generated/numpy.diff.html
   # The use of diff means we're passing an array of consecutive differences
   # to the max_min function.  diff is limited to differences of consecutive integers.
   # We'll use the max_min function to find that value across broader intervals.
   return ret_max_min_values(input, np.diff(input), limit)

# returns x position where gradient (slope) > limit.
def find_gradient(input, spacing, limit):
   # https://docs.scipy.org/doc/numpy/reference/generated/numpy.gradient.html
   # https://stackoverflow.com/questions/24633618/what-does-numpy-gradient-do
   # The use of gradient means we're passing an array of slopes to the max_min function.
   # Gradient by default computes the difference between values on either side of the 
   # index you pass to it, as opposed to diff, which looks at consecutive integers.
   return ret_max_min_values(input, np.gradient(input, spacing), limit)

# If we find a section where the gradient is greater than the allowed value,
# find the local maximum and minimum values and return them.
def ret_max_min_values(input, grad_array, limit, arr_range = 6):

# using a dictionary instead of a list, as dictionary items must be unique:
# https://www.w3schools.com/python/python_dictionaries.asp
   x_pos_array = {}
   
   for i in range(len(grad_array)):
      if abs(grad_array[i]) > limit:
         # for each value, construct temp array and return
         # both the max and min coordinates and values.
         temp_array = input[i-arr_range:i+arr_range+1]

         #x_pos_array_row = []
         # construct a list of the minimum index and minimum
         # value from a range around a high gradient array
         min_index, min_value = min(enumerate(temp_array), key=operator.itemgetter(1))
         min_index = i - arr_range + min_index         
         x_pos_array[min_index] = min_value

         #x_pos_array_row = []
         # and do the same for maximums
         max_index, max_value = max(enumerate(temp_array), key=operator.itemgetter(1))
         max_index = i - arr_range + max_index         
         x_pos_array[max_index] = max_value
         
         # x_pos_array should now contain the local minimum and maximum index and value

   return x_pos_array

def main():

   if len(sys.argv) < 3:
      print("function signature: identify-max-min.py input-file output-file")
      return 1

   infile = sys.argv[1]
   outfile = sys.argv[2]

   with open(infile) as f:
      input = np.array(map(int, f))

   overshoot_points = find_diff(input, limit=15)
   #overshoot_points = find_gradient(input, spacing=5, limit=2.5)

   with open(outfile,'w') as f:
      for key in sorted(overshoot_points.keys()):
         f.write("{},{}\n".format(key, overshoot_points[key]))
         print(key)   
   
if __name__ == '__main__':
    main()