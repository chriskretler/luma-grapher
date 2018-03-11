with open('line.txt') as f:
   array = map(int, f)

for i in range(0, len(array)):

   # If a luma value is less than 30, enter the fixing loop.
   if array[i] < 30:
      max_value = max(array[i:i+8])
      max_index = array.index(max_value)

      # set a floor of 30 as min_value
      if max_value < 30:
         max_value = 30

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
