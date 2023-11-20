#!/bin/sh
# /etc/init.d/crystalball.sh
### BEGIN INIT INFO
# Provides:          crystalball.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

# install with: sudo update-rc.d crystalball.sh defaults 

# wait for network to connect
sleep 5 && /usr/bin/python3 /home/queso/src/crystalball/server.py > /tmp/bootservice.log 2>&1

