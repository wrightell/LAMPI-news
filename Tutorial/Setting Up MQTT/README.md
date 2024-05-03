### Step 1: Getting MQTT
First we need to install MQTT on both our Lampi and EC2 instance. Run:
```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients -y
sudo pip3 install paho-mqtt==1.6.1
```
on both devices to get mosquitto, the service to run MQTT, and Paho and python library which handles MQTT communication.

### Step 2:
Our lampi is going to communicate to our ec2 instance with mqtt so we need to set up a bridge configuration. On the pi, run `sudo nano /etc/mosquitto/conf.d/bridge.conf` and copy the following:
```
connection b827eb309ede_broker
address <EC2_IP>:50001
remote_clientid b827eb309ede_broker
topic news out 1 "" devices/b827eb309ede/
cleansession true
```
This will create a connection with the name `b827eb309ede_broker`, which is the MAC address of this pi and then _broker. It is not necessary for this project but just in case someone wants to extend this project to mulpitple pi
s they can keep the naming convention of <'MAC ADDRESS'>_broker. Then we want to communicate to our EC2 instance so we write the ip followed by the port number. WARNING: this is an insecure port, and this project will not go over how to secure it. By default, mqtt uses 1883 so we must remeber to use this port for communication. We must map the topic `news` to outward connections only with qos 1 and add the prefix for good topic hierarchy. 

### Move on to [Setting Up Kivy GUI](../Setting%20Up%20Kivy%20GUI)
