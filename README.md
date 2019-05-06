# monitoring-dashboard
A dashboard displaying the performance of any server.


## Requirements

* Python3
* Sqlite3 (no need to install. It will be created by default)
* Redis (for scheduling alarms notifications)

```
$pip install -r requirements.txt
```

To run in production, change the PRODUCTION variable in manage.sh to True.

To get the data from the server, check out https://github.com/shubhamdipt/server-monitoring .


## Usage

### Create a superuser for login.
```
$./manage.sh createsuperuser
```

### Initiate the web server
```
$./manage.sh runserver
```

### Adding a device
* Add IP address of your device to Device model.
* The data coming from the device gets added to the DeviceData model.
* In the admin index page, then you can visualize the graphs of all devices.

### Creating an alarm
* Create a notification channel first.
* Create an Alarm.
* Finally create a Device Alarm corresponding to a certain device.

On creation of a device alarm, it creates a scheduled task based on the frequency provided.

### NOTE
**Device Alarm** : The frequency must be higher than or equal to the frequency (interval) of the incoming data from the 
respective Device added in the Device Alarm.

**Device Alarm for DOWNTIME**: The respective alarm comparison value(i.e. time period) entered should be higher than the frequency (interval) of the incoming data from the 
respective Device added in the Device Alarm.

![Sample of the Admin page](https://github.com/shubhamdipt/monitoring-dashboard/blob/master/sample.png)
