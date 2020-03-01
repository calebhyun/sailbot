import math
import py_qmc5883l
from time import sleep
from gps import *
import time
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
long1 = -122.4652
lat1 = 47.358435
tolerancelat = .0001
toleranellong = .0001
#houselat = 47.342257833 	
#houselong = -122.326749667 	

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
sensor = py_qmc5883l.QMC5883L()
def goLeft():
    print("LEFT")
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
def goRight():
    print("RIGHT")
    GPIO.output(32, GPIO.LOW)
    GPIO.output(36, GPIO.HIGH)
def goStraight():
    print("RIGHT")
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.HIGH)
def goForwards():
    print("Forwards")
    GPIO.output(38, GPIO.LOW)
def stop():
    GPIO.output(38, GPIO.HIGH)
def atTarget(pointA, pointB):
    float(getattr(report,'lon',0.0) - long1 < tolerancelong
    float(getattr(report,'lat',0.0)) - lat < tolerancelat
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

goForwards()
while atTarget == False:
    m = sensor.get_magnet()
    report = gpsd.next()
    if report['class'] == 'TPV':    
        heading = sensor.get_bearing()
        projectedHeading = (calculate_initial_compass_bearing((long1,lat1), ((float(getattr(report,'lon',0.0))),float(getattr(report,'lat',0.0)))))
        necessarychange = projectedHeading-heading
        
        
        #print(projectedHeading)
        #print(heading)
        #print(necessarychange)      
        if necessarychange >= 10:
            goLeft()
        elif necessarychange <= -10:
            goRight()
        else:
            goStraight()
stop()



