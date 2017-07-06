#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
DIR=`dirname $DIR`
INSTALL_DIR=`dirname $DIR`

apt-get install -y \
    libopenmpi-dev openmpi-bin \
    libsundials-serial-dev libsundials-serial \
    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
    git python-pip \
    gcc make \
    unzip wget \
    libfreetype6-dev libpng12-dev python-dev python-setuptools git subversion gfortran g++ gcc make pkg-config unzip wget apache2 libapache2-mod-wsgi npm nodejs-legacy graphviz realpath

pip install pip --upgrade
easy_install -U distribute


pip install -r $INSTALL_DIR/requirements.txt

cd $INSTALL_DIR

bower --allow-root install

cd $EXEC_DIR
