#!/bin/bash
set -e
DJANGODIR=$(dirname $(dirname $0))
NUMBER_DAYS=15

LOGFILE=$DJANGODIR/logs/purge_user_locations.log
LOGDIR=$(dirname $LOGFILE)

cd $DJANGODIR
source ../bin/activate
source deployment/local.sh

test -d $LOGDIR || mkdir -p $LOGDIR
exec ./manage.py purge_location_history $NUMBER_DAYS >> $LOGFILE
