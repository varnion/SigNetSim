#!/bin/bash

RETURN_APACHE=`wget -q -O - localhost:80/success | tail -n 1`
echo "> Apache returned : ${RETURN_APACHE}"
RES=`expr $RETURN_APACHE == SUCCESS`
RETURN_APACHE_STATIC=`wget -q -O - localhost:80/static/success | tail -n 1`
echo "> Apache returned : ${RETURN_APACHE_STATIC}"
RES_STATIC=`expr $RETURN_APACHE_STATIC == SUCCESS`

echo "Return Apache : " $RETURN_APACHE
echo "Return Apache static : " $RETURN_APACHE_STATIC

if [ "$RES" = 1 ] && [ "$RES_STATIC" = 1 ]; then
	exit 0;
else
	exit 1;
fi