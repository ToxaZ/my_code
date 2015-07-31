__author__ = 'ToxaZ'

import sys

prev_user_id = None
user_events = []

for line in sys.stdin:
    user_id, event, date = line.strip().split(sep=',')
    if prev_user_id is None:
        prev_user_id = user_id
        user_events = [event]
        prev_event = event
    elif user_id != prev_user_id:
        sys.stdout.write(','.join(user_events)+'\n')  # printing lines
        prev_user_id = user_id
        user_events = [event]
        prev_event = event
    else:
        user_events.append(event)
        prev_event = event
        prev_user_id = user_id

sys.stdout.write(','.join(user_events)+'\n')  # printing last line
