import numpy as np
from numpy import genfromtxt
import sys

# This script takes an input file that VHS edge over enhancement
# thas has been previously identified by one of the identify scripts.
# it uses the points from the 'overshoot_points' file as input and fixes
# those points via averaging.

def snippet_to_smooth(rng):
   sections = []

   for i in genfromtxt('./overshoot_points.txt', delimiter=',')[:,0]:
      #print("i is: {}", i)
      for j in range(rng*2):
         #print("j is: {}", j)
         sections.append(int((i+j)-5))
   return np.unique(sections)


def average_sections(input, overshoot_points, radius):
   output = input

   for i in overshoot_points:
      if i + radius + 1 <= len(input):
         temp_array = input[i-radius:i+radius+1]
         output[i] = np.average(temp_array)
   return output


def main():
   file = sys.argv[1]

   with open(file) as f:
      input = np.array(map(int, f))

   # We previously had to sort the input overshoot points. This is now being done
   # within the identify files, we shouldn't need to do this anymore.
   overshoot_points = snippet_to_smooth(rng=6)
   #overshoot_points = genfromtxt('./overshoot_points.txt', delimiter=',')[:,0]
   print(overshoot_points)
   
   smoothed = average_sections(input, overshoot_points, radius=7)
   #print smoothed

   np.savetxt("../output/Sather-averaging.txt", smoothed, fmt='%i', delimiter="\n")

if __name__ == '__main__':
    main()
