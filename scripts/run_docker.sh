#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`
DATA_DIR=$1

docker build -t signetsim:xenial $DIR/docker
RUN /bin/bash /SigNetSim/scripts/install.sh

if [[ -z "${DATA_DIR}" ]]
then
    docker run -d --name signetsim_container -p 8080:80 signetsim:xenial usr/sbin/apache2ctl -D FOREGROUND
else
    docker run -d --name signetsim_container -p 8080:80 \
                -v ${DATA_DIR}/data:/SigNetSim/data \
                -v ${DATA_DIR}/settings:/SigNetSim/settings \
                signetsim:xenial usr/sbin/apache2ctl -D FOREGROUND
fi

docker exec signetsim_container /bin/bash /SigNetSim/scripts/apache/generate_apache.sh
docker exec signetsim_container /bin/bash /SigNetSim/scripts/apache/install_apache.sh
docker exec signetsim_container /bin/bash /SigNetSim/scripts/create_db.sh