#!/bin/bash
/usr/sbin/cron
service ssh start &
exec apache2-foreground 
echo "YOOO"
wait -n
exit $?
