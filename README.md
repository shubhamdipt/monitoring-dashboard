# monitoring-dashboard
A dashboard displaying the performance of any server.


## Requirements

* Python3
* Sqlite3
* Redis (for scheduling alarms notifications)

```
$pip install -r requirements.txt
```

To run in production, change the PRODUCTION variable in manage.sh to True.

To get the data from the server, check out https://github.com/shubhamdipt/server-monitoring .


## Usage
```
$./manage.sh runserver
```

### Creating a device
* Add IP address of your device to Device model.
* The data coming from the device gets added to the DeviceData model.
* In the admin index page, then you can visualize the graphs of all devices.

### Creating an alarm
* Create a notification channel first.
* Create an Alarm.
* Finally create a Device Alarm corresponding to a certain device.

On creation of a device alarm, it creates a scheduled task based on the frequency provided.

![Sample of the Admin page](https://github.com/shubhamdipt/monitoring-dashboard/blob/master/sample.png)