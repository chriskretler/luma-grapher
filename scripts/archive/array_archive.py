import numpy.lib as stride_tricks
from itertools import islice

# shape defines the dimensions of the new temp array.
# strides define memory-based coordinates of original array items.
def pystride(array,frame_length,strided_items):
   num_frames = 1 + ((len(array) - frame_length)/ strided_items)
   row_stride = array.itemsize * strided_items
   col_stride = array.itemsize

   a_strided = np.lib.stride_tricks.as_strided(
      array,
      shape=(num_frames, frame_length),
      strides=(row_stride, col_stride)
   )
   return a_strided

# looks like we can simply change the array value via:
# https://docs.python.org/2.3/whatsnew/section-slices.html
def it_slice(array):
   it = iter(array)

   result = tuple(islice(it,15))
   print result
   it.next()

   result = islice(it,15)
   print result

def find_max_min(array):
   max_diff = 120

   for sub in pystride(array,frame_length=7,strided_items=2):
      max_val = max(sub)
      min_val = min(sub)
      if abs(max_val - min_val) >= max_diff:
         # assign 'pointers' in original array indicating where large diffs are found.
         sub[0] = int('{:<05}'.format(sub[0]))

#find_max_min(array)
#for i in range(0, len(array)):
#   if array[i] <= 30:
#      myArray = np.array([i,i+1,i+2,i+3,i+4,i+5,i+6,i+7,i+8])
#      max = localMax(myArray)
