import csv
import numpy as np
import operator
import sys

# returns x position where average diff across spacing > limit.
def plot_diff(input, points, window):
   # https://docs.scipy.org/doc/numpy/reference/generated/numpy.diff.html
   # The use of diff means we're passing an array of consecutive differences
   # to the max_min function.  diff is limited to differences of consecutive integers.
   # We'll use the max_min function to find that value across broader intervals.
   # points at this point ONLY contains the coordinates, not the values!!
   rational_points = {}
   
   for row in points:
      if row:
         row = row.split(',')
         point = int(row[0])
         value = int(row[1])
         type = row[2]

         grad = np.diff(input[point:point + window])
         #grad = np.gradient(input[point:point + window], 2)
         if type=='min':
            for i in range(window-1):
               # skip the first four pixels, then look for gradients
               # with an absolute value below a certain value.
            
               if i >= 4:
                  #print("{}".format(grad[i]), end=',')
                  if grad[i] < 0:
                     rational_points[point + i] = value
                     break

   return rational_points

def main():

   if len(sys.argv) < 4:
      print("function signature: identify-rational-after-min.py input-file overshoot-points-file output-file")
      return 1

   # the infile contains the values of pixels, but not their location. It's implied.
   infile = sys.argv[1]
   # The points file contains the location of relative max and min, but not their values.
   points_file = sys.argv[2]
   # the outfile will contains the placement and value of first rational pixels after overshoot
   outfile = sys.argv[3]

   with open(infile) as f:
      # this returns an array of ints from the input file.
      input = [int(x) for x in f.read().split('\n') if x]
   
   with open(points_file) as pf:
      points = pf.read().split('\n')

   # Find the slope within n pixels to the right of local minimums.
   rational_points = plot_diff(input, points, window=12)

   with open(outfile,'w') as f:
      for key in sorted(rational_points.keys()):
         f.write("{},{}\n".format(key, rational_points[key]))
         print(key)   
   
if __name__ == '__main__':
    main()