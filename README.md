# Camera_vision

## Usage of init script
This module can be run from userspace by invoking the
'service' or 'sysctl' Linux commands.

```
Usage: /etc/init.d/camera.sh {start|stop|restart}"
```

after cloning the module, users should place the 'camera'
init script into `/etc/init.d`. init scripts should be run
by root:

```shell
sudo chown root:root /etc/init.d/camera
```

and permission to execute should be set:

```shell
sudo chmod 755 /etc/init.d/camera
```

reload the runcom configuration:

```shell
sudo update-rc.d -f camera defaults
```

the script can now be used with the service command and
will start on boot of the Raspberry Pi.
