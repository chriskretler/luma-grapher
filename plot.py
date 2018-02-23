import matplotlib.pyplot as plt

#f = open('line.txt')
#for line in f.readline():
#    print line
#f.close()
with open('line.txt') as f:
   array = map(int, f)

#print array
#plt.plot([64,65,63,64])
plt.plot(array)
#plt.plot(1, 2, 3, 4], [64,65,63,64], 'b-')
plt.axis([0, 8, 0, 255])

plt.ylabel('Luma Values')
plt.show()