#!/usr/bin/env bash

cat $path | # source file path
python mapper.py |
sort -k 1,1 |
python reducer.py $sep