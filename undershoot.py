with open('line.txt') as f:
   array = map(int, f)

for i in range(0, len(array)):
   if array[i] < 30:
      subarray = array[i:i+6]
   print len(subarray)
   #print array[i]