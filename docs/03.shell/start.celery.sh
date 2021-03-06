#!/bin/bash

ps -ef|grep celery |grep -v grep |grep -v sh| awk '{print $2}'| xargs kill -9

unset PYTHONPATH
cd ../../gk7/
mkdir logs
../env/bin/celery -A task.tasks worker -l info -D -f logs/gk7-douban.log --pidfile=logs/celery.pid
