Requirement 1 & 2

We have placed the following four lines in
 /etc/rc.local
on the Pi to setup ad-hoc on boot 

Set the wifi interface to have type ibss instead of managed:

sudo iw wlan0 set type ibss

Set the wifi interface active:

sudo ip link set wlan0 up

Create a wifi network with ssid pibot on channel 11 (2462MHz):

sudo iw wlan0 ibss join pibot 2462

Add static IP address to the wifi interface:

sudo ip address add 192.168.99.9/16 dev wlan0


To join the ad-hoc network on the Pi, the following lines is entered
in shell on laptop:

Create a new interface so the laptop still would be able to join
a wifi network without reverting everything:

sudo iw phy phy0 interface add ibs0 type ibss

Set type of ibs0 interface to ibss if it is not already:

sudo iw ibs0 set type ibss

Set a static IP on the ibs0 interface so the laptop is able to find and join
the Pi's ad-hoc network:

sudo ip address add 192.168.99.5/16 dev ibs0

Set the interface active:

sudo rfkill unblock wifi
sudo ip link set ibs0 up

Join the pibot network:

sudo iw ibs0 ibss join pibot 2462



Requirement 3

The TCPServer.py includes TCP server creation with multithreading.
This was necessary to be able to send stop command if the robot had started
with enters an infinite while loop.
All four commands, 'getdist' 'getmotors' 'start' and 'stop' all works as intended.

The functions can be called by echoing to the TCP server using socat:
Example:
	echo start | socat - tcp:192.168.99.9:8080
	
will start the "follow wall" code.

The name TCPServer.py is a bit misleading as the functions to 
run the robot also is included in this python script.


Requirement 4

The bot is not really able to follow the wall as it is more set to be 
avoiding the wall.
Time ran out so we weren't able to change the code enough to 
make it follow the wall.
