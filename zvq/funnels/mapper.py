__author__ = 'ToxaZ'

import sys
import json

log = open('missed_events.log', 'w')

for line in sys.stdin:
    json_input = json.loads(line)
    try:
        sys.stdout.write('\t'.join([str(json_input['properties']['app_instance']),
                                   str(json_input['event']),
                                   str(json_input["packet_date"])]) + '\n')
    except KeyError:
        log.write(line)

log.close()
