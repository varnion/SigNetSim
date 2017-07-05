#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

cd ${INSTALL_DIR}

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p data/db
    mkdir -p data/media

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

    echo "from signetsim.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

else

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

fi

chgrp -R www-data data
chmod -R 664 data
find data -type d  -exec chmod 775 {} \;

cd $EXEC_DIR
