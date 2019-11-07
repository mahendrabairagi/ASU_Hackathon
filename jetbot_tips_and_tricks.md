# Jetbot Tips & Tricks
The following are a set of recipes that will help you dive deeper into the operation of jetbot and understand how your ROS application is functioning.

### Connecting to your Jetbot
The ip address of your jetbot on the local network is displayed on the OLED display of the robot.

From you local machine, type the following to open an SSH conenction to your robot:
```
# connect to the jetbot
$ ssh jetbot@<ip-address>
```

### Copying a files to the jetbot

From your local machine:
```
# to copy files TO the jetbot
$ scp /path/to/local/file jetbot@<ip-address>:/home/jetbot/<some-path>

# copy files FROM the jetbot
$ scp jetbot@<ip-address>:/home/jetbot/<some-patn> /path/to/local/file
```

-----

All of the following commands assume you have connected to the Jetbot.


## Greengrass

### Add Greengrass certificates
AWS Greengrass uses X.509 certificates, managed subscriptions, AWS IoT policies, and IAM policies & roles to secure the applications that run on robots in your deployment environment.

An AWS RoboMaker robot is also a Greengrass core. Core devices use certificates and policies to securely connect to AWS IoT. The certificates and policies also allow AWS IoT Greengrass to deploy configuration information, Lambda functions, connectors, and managed subscriptions to core devices.


From your local machine:
```
# Copy security resources from your local machine to the robot
$ scp /path/to/downladed-zip/<robot-certs>.zip jetbot@<ip-addres>:/home/jetbot/robomaker-robot-certs.zip
```

Connected to the jetbot:
```
# Switch to the root user
$ sudo su -s /bin/bash

# Unzip the jetbot security credentials to greengrass certificate store
$ unzip /home/jetbot/robomaker-robot-certs.zip -d /greengrass/ggc/certs
```

### Starting & Stopping Greengrass
Starting and stopping the greengrass daemon can be performed as follows:

```
# switch to the root user
$ sudo su -s /bin/bash

# start the daemon
$ /greengrass/ggc/core/greengrassd start

# stop the daemon
$ /greengrass/ggc/core/greengrassd stop
```

### Viewing Greengrass logs
AWS Greengrass provides both system logs and user logs to inspect functionality
```
# switch to the root user
$ sudo su -s /bin/bash

# change to the greengrass log directory
$ cd /greengrass/ggc/var/log

# tail the runtime log
$ tail -f system/runtime.log

# press Ctrl-C to exit tailing the file
```


## Robomaker

### Viewing ROS runtime logs
When developing new functionality or diagnosing bugs, it is often helpful to both log data and output state.  These messages are captured by the ROS application and stored on the local filesystem.

```
# change to the ros deployment direcotry
$ cd /home/ggc_user/ros/home

# log files for each Robomoaker deployment are stored in separate directories
# e.g. deployment-652q4b4ckt7p (your most recent deployment will vary)
$ cd  deployment-652q4b4ckt7p/log/latest/

** NOTE: put an example tree here**

# view the log file
cat circle-2.log

** NOTE: put an example log file here
```





