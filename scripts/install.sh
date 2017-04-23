#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

cd $INSTALL_DIR

pip install -r requirements.txt

mkdir -p data/db
mkdir -p data/media

bower --allow-root install

mkdir -p signetsim/static/mpld3
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/d3.v3.min.js signetsim/static/mpld3/
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/mpld3.v0.3.min.js signetsim/static/mpld3/
mkdir static

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput > /dev/null
echo "from signetsim.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
