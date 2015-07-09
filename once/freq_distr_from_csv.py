__author__ = 'toxaz'

import numpy as np

file = open('data.csv', 'r')
duration = []

for line in file:
    values = line.split(',')
    if int(values[1][-2]) > 1:
        duration.append(int(float(values[0])))

print len(np.bincount(duration))

np.savetxt('hist.csv', np.asarray(np.bincount(duration)), delimiter=',', header='count, value')