#!/usr/bin/env bash
export PYTHONPATH="/home/toxaz/Work/Repos/my_code/"

scp az@f1:/var/log/nginx/nginx-pixel.log* ./
gunzip nginx-pixel.log*.gz

cat nginx-pixel.log-* >> nginx-pixel.log

set +u

python2.7 -m beestats.pixelparser "nginx-pixel.log" "landing_events.json"

set -u

rm nginx-pixel.log*
rm landing_events.json
