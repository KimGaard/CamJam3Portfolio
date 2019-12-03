import socket
import sys
import _thread
import time  # Import the Time library
from gpiozero import CamJamKitRobot, DistanceSensor  # Import the GPIO Zero Libraries

# Define GPIO pins to use for the distance sensor
pintrigger = 17
pinecho = 18

robot = CamJamKitRobot()
sensor = DistanceSensor(echo=pinecho, trigger=pintrigger)

# Distance Variables
hownear = 20.0
howfar = 30.0
reversetime = 1
turntime = 0.25

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.30
rightmotorspeed = 0.30

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorleft = (leftmotorspeed + 0.2, 0)
motorright = (0, rightmotorspeed + 0.2)


# Return True if the ultrasonic sensor sees an obstacle
def isnearobstacle(localhownear):
    distance = sensor.distance * 100

    print("IsNearObstacle: " + str(distance))
    if distance < localhownear:
        return True
    else:
        return False
def followwall():
    print("Backwards")
    robot.value = motorbackward
    time.sleep(reversetime)
    robot.stop()
    time.sleep(0.75)
           
    print("Right")
    robot.value = motorright
    time.sleep(turntime)
    robot.stop()        
    leftmotorspeed = 0.35

    
def getdist():
    distance = sensor.distance * 100
    return distance

def getmotors():
    return leftmotorspeed, rightmotorspeed

startrobot = False
def start():
    # Your code to control the robot goes below this line
    try:
        # repeat the next indented block forever
        while startrobot:
            robot.value = motorforward
            time.sleep(0.1)
            if isnearobstacle(hownear):
                robot.stop()
                followwall()

    # If you press CTRL+C, cleanup and stop
    except KeyboardInterrupt:
        robot.stop()


def stop():    
    robot.stop()


    
# TCP server
host = ''
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

try:
    s.bind((host, port))
except socket.error:
    print("Binding failed")
    sys.exit()

print("Socket bind complete")

s.listen(5)

print("Socket is ready")

def clientthread(conn):
    while True:
        data = conn.recv(1024)

        if not data:
            break

        
        decodedData = data.decode().rstrip("\n").split(" ")
        print("Recieved data: " + decodedData[0])
        global startrobot
        if decodedData[0] == "start":
            startrobot = True
            start()
            respons = "Robot started\n"            
            conn.send(str.encode(respons))
            
        elif decodedData[0] == "stop":
            startrobot = False
            stop()
            respons = "Robot stopped\n"
            conn.send(str.encode(respons))
            
        elif decodedData[0] == "getdist":
            respons = "Distance is: " + str(getdist()) + "\n"
            conn.send(str.encode(respons))
            
        elif decodedData[0] == "getmotors":
            respons = "Motor values is" + str(getmotors()) + "\n"
            conn.send(str.encode(respons))
            
        else:
            respons = "Command not valid\n"
            conn.send(str.encode(respons))
            
            
    conn.close()
    
while True:
    conn, address = s.accept()
    print("Connected with: " + address[0] + ":" + str(address[1]))
    _thread.start_new_thread(clientthread, (conn,))


s.close()
