#!/usr/bin/env bash
if [ -z "${BIN+x}" ] ; then
 echo "require env \$BIN"
 exit
fi
INSTALL=$BIN/poi
rm -f $INSTALL

echo "complate"
