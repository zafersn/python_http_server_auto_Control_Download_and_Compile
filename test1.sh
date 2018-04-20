#!/bin/bash
echo "klasore giriliyor..."
cd ThreadControl
echo "derleme surumu ayarlaniyor... 1.76"
export CFLAGS=-DSW_VERSION=\\\"1.7.26\\\" 
echo "make yapiliyor..."
make
echo "make install yapiliyor.."
make install
echo "kill yapiliyor..."
pkill -f ttymxc5
echo  "usb baglantilar listeleniyor..."
ps -ef | grep tty*
/usr/bin/ThreadDeviceMgr /dev/ttymxc5 fslthr0 tap 0
echo "tamamlandi cikiliyor..."
exit 0
