#!/bin/bash

set -e
DJANGODIR=$(dirname $(dirname $0))
DJANGO_WSGI=trytalk.wsgi
DJANGO_SETTINGS_MODULE=trytalk.settings.production
GUNICORN_CONFIG=$DJANGODIR/scripts/gunicorn_config.py

LOGFILE=$DJANGODIR/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)

cd $DJANGODIR
source ../bin/activate
source deployment/production.sh

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -c $GUNICORN_CONFIG \
  --log-level=info \
  --log-file=$LOGFILE \
  $DJANGO_WSGI 2>> $LOGFILE
