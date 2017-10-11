#!/usr/bin/env bash
if [ -z "${BIN+x}" ] ; then
 echo "require env \$BIN"
 exit
fi
INSTALL=$BIN/poi
rm -f $INSTALL
ln -s $(pwd)/poi.py $INSTALL

echo "complate"
