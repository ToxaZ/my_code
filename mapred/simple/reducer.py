__author__ = 'az'

import sys

values = 0
prev_key = None

for line in sys.stdin:
    key, value = line.split(sep=sys.argv[0])
    if key == (prev_key or None):
        values += value
        prev_key = key
    else:
        print (key, " ", values)
        values = 0
        prev_key = key