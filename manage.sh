#!/bin/sh

DJANGO_SETTINGS_MODULE="monitoringdashboard.settings"
#PRODUCTION=true
SECRET_FILE="./.secret.key"
SECRET_LENGTH=32

# Create the secret file if it does not exist, otherwise NOP
[ -r $SECRET_FILE ] || < /dev/urandom LC_ALL=C tr -d -c "[:punct:][:alnum:]" | 2>/dev/null dd count=1 bs=$SECRET_LENGTH > $SECRET_FILE

# Call the manage.py with the right environment variables (and don't leak them)
if [ "$PRODUCTION" = true ]
then
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PRODUCTION=$PRODUCTION
    export SECRET_KEY="$(cat $SECRET_FILE)"
    mkdir -p static
    if [ "$1" = "runserver" ]
    then
        python3 manage.py collectstatic --clear --noinput -v0
        nohup sh -c "uwsgi --ini uwsgi.ini" > /dev/null 2>&1 &
    else
        python manage.py $@
    fi
else
    DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE \
    PRODUCTION=$PRODUCTION \
    SECRET_KEY="$(cat $SECRET_FILE)" \
    python manage.py $@
fi
