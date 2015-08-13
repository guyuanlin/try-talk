#!/bin/bash
set -e
DJANGODIR=$(dirname $(dirname $0))

LOGFILE=$DJANGODIR/logs/push_demo_notification.log
LOGDIR=$(dirname $LOGFILE)

cd $DJANGODIR
source ../bin/activate
source deployment/production.sh

test -d $LOGDIR || mkdir -p $LOGDIR
exec ./manage.py push_demo_notification >> $LOGFILE
