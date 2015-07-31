__author__ = 'ToxaZ'

import sys
import json

for line in sys.stdin:
    json_input = json.loads(line)
    sys.stdout.write(','.join(
        [str(json_input['properties']['user_id']), str(json_input['event']), str(json_input["packet_date"])])+'\n')
