#!/usr/bin/env bash
#
#export  PYTHONPATH=/usr/app/entity_spider:/user/app/entity_spider/api
#echo  $PYTHONPATH

set -e
case $1 in
    worker)
    exec celery -A entity_spider.CeleryApp worker -l info
    ;;


    beat)
	exec celery -A entity_spider.CeleryApp beat -l debug
    ;;


esac
