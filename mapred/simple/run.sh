#!/usr/bin/env bash

cat $1 |  # source file path
python3 mapper.py |
sort -k 1,1 |
python3 reducer.py $2 | # define separator
sort -r -k 2,2