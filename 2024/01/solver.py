import numpy as np

f = open("input.txt", "r")
lines = f.readlines()

list1 = []
list2 = []

for line in lines:
    line = line.replace("\n", "")
    if line != "":
        values = line.split("   ")

        list1.append(int(values[0]))
        list2.append(int(values[1]))

list1.sort()
list2.sort()

vector1 = np.array(list1)
vector2 = np.array(list2)

sum_vector = abs(vector1 - vector2)


score = 0
for item in np.unique(list1):
    score += item * np.count_nonzero(list2 == item)



print(np.sum(sum_vector))
print(score)