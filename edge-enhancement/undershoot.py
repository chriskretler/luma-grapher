with open('line.txt') as f:
   array = map(int, f)

for i in range(0, len(array)):

   # If a luma value is less than 30, enter the fixing loop.
   if array[i] < 30:
      max_index = 0
      max_value = 0
      while max_value == 0:
         # iterate through defined number of pixels looking for a value > 30.
         # if you find one, break out of the array
         for v in array[i:i+6]:
            if v > 30:
               max_index = array.index(v)
               max_value = v
               break
         # set a floor of 30 as min_value
         if max_value < 30:
            max_value = 30
            max_index = i+6

      # assign all values from i to max_index = max_value
      for j in range(i, max_index):
         array[j] = max_value
         #print str(array[i]) + "," + str(i) + "," + str(max_value) + "," + str(max_index)
      i = j

f = open('new_line', 'w')

for i in array:
   f.write("%s\n" % i)
f.close()
#print array
