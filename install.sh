#!/usr/bin/env bash
if [ -z "${LOCAL_BIN+x}" ] ; then
 echo "require \$LOCAL_BIN"
 exit
fi
INSTALL=$LOCAL_BIN/poi
rm -f $INSTALL
ln -s $(pwd)/poi.py $INSTALL

echo "complate"
