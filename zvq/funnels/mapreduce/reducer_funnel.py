__author__ = 'ToxaZ'

import sys
from collections import OrderedDict

funnel = OrderedDict((str(x), 0) for x in sys.argv[1:])

for line in sys.stdin:
    user_events = line.rstrip('\n').split('\t')
    count_step = 0
    event_index = 0
    for event in funnel:
        try:
            event_index = user_events[event_index:].index(event)
            funnel[event] += 1
            count_step += 1
        except ValueError:
            count_step = 0
            break

sys.stdout.write(str(funnel)+'\n')
