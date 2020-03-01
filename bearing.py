import math
import py_qmc5883l
from time import sleep
from gps import *
import time
import RPi.GPIO as GPIO
import time
#Tahlequah Vashon Island
long1 = -122.516422
lat1 = 47.355398
tolerancelat = .00001
toleranellong = .00001
#houselat = 47.342257833 	
#houselong = -122.326749667 	
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
sensor = py_qmc5883l.QMC5883L()

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees.
        This should be the current location
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees.
        This should be the target location.
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

def atTarget(pointA, pointB):
    if abs(pointA[0]-pointB[0]) < tolerancelat and abs(pointA[1]-pointB[1]) < tolerancelong:
        return True
    else:
        return False

#while atTarget == False:

m = sensor.get_magnet()
report = gpsd.next()
while report['class'] != 'TPV':
    report = gpsd.next()
    if report['class'] == 'TPV':
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))


print(atTarget((lat1,long1), (cur_lat, cur_long))) 
while atTarget((lat1,long1), (cur_lat, cur_long)) == False:
    m = sensor.get_magnet()
    report = gpsd.next()
    if report['class'] == 'TPV':    
        heading = sensor.get_bearing()
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))
        projectedHeading = calculate_initial_compass_bearing((cur_lat,cur_long), (lat1, long1))
        necessarychange = projectedHeading-heading
        print(projectedHeading, heading, necessarychange)
        
        #print(projectedHeading)
        #print(heading)
        #print(necessarychange)      
        if necessarychange >= 10:
            print("goLeft()")
        elif necessarychange <= -10:
            print("goRight()")
        else:
            print("goStraight()")
        time.sleep(.1)
        #stop()
        time.sleep(.1)



