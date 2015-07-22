#!/bin/bash
set -e
DJANGODIR=$(dirname $(dirname $0))

LOGFILE=$DJANGODIR/logs/purge_requests.log
LOGDIR=$(dirname $LOGFILE)

cd $DJANGODIR
source env/bin/activate
source deployment/production.sh

test -d $LOGDIR || mkdir -p $LOGDIR
exec ./manage.py purgerequests 2 weeks --noinput >> $LOGFILE
