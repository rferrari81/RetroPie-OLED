#!/usr/bin/env bash
# edited by zzeromin ( 2016-10-14 )
# special thanks to zerocool
# Reference:
# runcommand of Retorpie:  https://github.com/retropie/retropie-setup/wiki/runcommand
# edit and path: $ sudo nano /opt/retropie/configs/all/runcommand-onend.sh

sed '1,$d' /dev/shm/runcommand.log > /dev/shm/runcommand.log
echo "notice" >&2
echo "RetroPie" >&2
echo "SysInfo" >&2