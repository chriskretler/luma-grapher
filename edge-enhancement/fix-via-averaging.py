import numpy as np
from datetime import datetime
from numpy import genfromtxt
import logging

logger = logging.getLogger('undershootFiller')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('processing.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)


time1 = datetime.now()

with open('Sather-line-352-original.txt') as f:
   array = np.array(map(int, f))

def snippet_to_smooth(rng):
   sections = []

   for i in genfromtxt('overshoot_points.txt', delimiter=',')[:,0]:
      for j in range(rng*2):
         sections.append(int((i+j)-5))
   return np.unique(sections)


def average_sections(array, overshoot_points, radius):
   for i in overshoot_points:
      logger.info('i is: ' + str(i))
      if i + radius + 1 <= len(array):
         logger.info('input is: ' + str(array[i]))
         temp_array = array[i-radius:i+radius+1]
         logger.info('temp_array is: ' + str(temp_array))         
         array[i] = np.average(temp_array)
         logger.info('output is: ' + str(int(np.average(temp_array))))
   return array

overshoot_points = snippet_to_smooth(6)
smoothed = average_sections(array, overshoot_points, radius=7)
#print smoothed

np.savetxt("./output.txt", smoothed, fmt='%i', delimiter="\n")

time2 = datetime.now()
print (time2 - time1)
