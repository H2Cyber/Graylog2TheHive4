# Graylog2TheHive4
A simple web application (Flask webhook) that listens for Graylog HTTP notifications, and transforms them into TheHive alerts.

# Environment
Graylog2TheHive4 has been tested with the following software versions :
* TheHive 4, installed on a Ubuntu 20.04 Server
* Graylog 4

Graylog2TheHive4 should be installed on the same server where TheHive is installed.

# Setup
## Create a new user in TheHive and grab its API key
Login to TheHive as a global administrator, navigate to the relevant organisation and create a new user.
Copy the new user's API key, which shall be used in the Graylog2TheHive4 configuration later.

## Install the required prerequisites
The required prerequisites can be installed on Ubuntu 20.04 using the following commands :
```
$sudo apt install python3-pip
$sudo python3 -m pip install thehive4py 
$sudo python3 -m pip install Flask
$sudo python3 -m pip install requests
```

## Create the web application that listens for Graylog requests
Create a new directory under `/opt` using the following commands, and set the right system permissions for it. Do not forget to change `yourusername` with your actual Ubuntu username :
```
$cd /opt
$sudo mkdir graylog2thehive4
$sudo chown -R yourusername:yourusername graylog2thehive4
```
Grab the [graylog2thehive4.py](https://github.com/H2Cyber/Graylog2TheHive4/blob/main/graylog2thehive4.py) file contents and copy them under the newly create directory: 
```
$nano /opt/graylog2thehive4/graylog2thehive4.py
```

Configure the following elements within `graylog2thehive4.py` :
* TheHive API key (created earlier), on line 18
* Graylog's URL, on line 22

The web application should be ready and can be tested as follows :
```
$export FLASK_APP=/opt/graylog2thehive4/graylog2thehive4.py
$python3 -m flask run --host=0.0.0.0
```

## Install the web application as a system service
Grab the [systemctl unit file](https://github.com/H2Cyber/Graylog2TheHive4/blob/main/graylog2thehive4.service) file contents and copy them under `/etc/systemd/system/graylog2thehive4.service` : 
```
$sudo nano /etc/systemd/system/graylog2thehive4.service
```

Make sure the service is enabled on startup using the following commands :
```
sudo systemctl daemon-reload
sudo systemctl enable graylog2thehive4.service
```
Start the service using the following command :
```
sudo systemctl start graylog2thehive4.service
```
## Create a new notification in Graylog
In Graylog, navigate to `Alerts > Notifications` and click on `Create Notification`.

Choose a Title and a Description for the new Notification, then select the notification type `HTTP Notification`.

The URL should respect the following format : http://THEHIVE-IP:5000/webhook (for example: http://10.10.10.100:5000/webhook).

Click on `Execute Test Notification`. A new Alert should appear in TheHive. 

# Credits
Credit goes to the original [graylog2thehive](https://github.com/ReconInfoSec/graylog2thehive) project for (most of) the code.
