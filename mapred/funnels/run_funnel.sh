#!/usr/bin/env bash

python3 mapper.py |
sort -k 1,3 |
python3 reducer_user_events.py |
python3 reducer_funnel.py $1 # list of funnel events in funnel order as string
