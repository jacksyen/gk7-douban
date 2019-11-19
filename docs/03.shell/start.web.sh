#!/bin/bash

cd ../../
source env/bin/activate
uwsgi --socket 127.0.0.1:9031 --wsgi-file gk7/index.py --master --enable-threads --processes 2 --daemonize gk7/logs/gk7-douban.log --pidfile gk7/logs/uwsgi.pid
