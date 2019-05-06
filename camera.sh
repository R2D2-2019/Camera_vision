#!/bin/bash
### BEGIN INIT INFO
# Provides:          /home/pi/camera.py
# Required-Start:    networking /home/pi/r2d2-python-build/manager/manager.py
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start RasPi camera module at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

NAME=camera
DAEMON=/home/pi/camera.py
PIDFILE=/var/run/camera.pid

# check if the module is present
if [ -f $DAEMON ]; then
	case "$1" in # "$1" denotes the first argument to the command
		start)
			echo "Starting camera module...";
			python3 /home/pi/camera.py;
			;; # break
		stop)
			echo "Stopping camera module...";
			pkill camera.py;
			;; # break
		restart)
			stop;
			start;
			;; # break
		*) # all other arguments (default)
			echo "Unsupported syntax:";
			echo "Usage: /etc/init.d/camera.sh {start|stop|restart}";
			exit 1;
	esac
else
	echo "The module is not present at $DAEMON";
	exit 1;
fi

exit 0;
