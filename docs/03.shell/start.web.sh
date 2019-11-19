#!/bin/bash

cd ../../
source env/bin/activate
cd gk7/

ps -ef|grep uwsgi|grep -v grep |awk '{print $2}'|xargs kill -9
../env/bin/uwsgi --socket 127.0.0.1:9031 --wsgi-file index.py --master --enable-threads --processes 2 --daemonize logs/gk7-douban.log --pidfile logs/uwsgi.pid
