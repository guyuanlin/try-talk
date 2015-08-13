#!/bin/bash
set -e
DJANGODIR=$(dirname $(dirname $0))
DJANGO_PROJECT_NAME=trytalk
DJANGO_SETTINGS_MODULE=trytalk.settings.production

LOGFILE=$DJANGODIR/logs/celery_worker.log
LOGDIR=$(dirname $LOGFILE)

cd $DJANGODIR
source ../bin/activate
source deployment/production.sh

test -d $LOGDIR || mkdir -p $LOGFILE
exec celery -A $DJANGO_PROJECT_NAME \
	worker --loglevel=info \
	2>>$LOGFILE