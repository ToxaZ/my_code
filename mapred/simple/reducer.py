__author__ = 'ToxaZ'

import sys

values = 0
prev_key = None

for line in sys.stdin:
    key, value = line.strip().split(sep=',')
    if prev_key != key:
        values += int(value)
        sys.stdout.write(key + " " + str(values)+ "\n")
        values = 0
        prev_key = key
    else:
        values += int(value)
        prev_key = key

