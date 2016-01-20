#!/usr/bin/env bash
# author - ToxaZ
# simple script to gather nginx access logs

sponsor=$1
rm "$sponsor".log

for backend in f5 f7 f8
do
    echo $backend
    {
    # ssh az@$backend.zvq.me "zgrep 'GET /napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log-201512*.gz" | cut -c 48- 
    ssh az@$backend.zvq.me "zgrep 'GET /napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log-201601*.gz" | cut -c 48- 
    ssh az@$backend.zvq.me "fgrep 'GET /napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log"
    } >> "$sponsor".log 
done
