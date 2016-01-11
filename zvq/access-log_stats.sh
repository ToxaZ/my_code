#!/usr/bin/env bash

sponsor="ulmart"

for backend in f5 f7 f8
do
    echo $backend
    ssh az@$backend.zvq.me "zgrep 'napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log-2015123*.gz" | cut -c 48- >> $sponsor.log
    ssh az@$backend.zvq.me "zgrep 'napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log-20160101.gz" | cut -c 48- >> $sponsor.log
    ssh az@$backend.zvq.me "fgrep 'napi/sponsor-offers/$sponsor' /var/log/nginx/zvooq.ru-access.log" >> $sponsor.log
done
