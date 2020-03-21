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
sensor.calibration = [[1.013535132361361, -0.008522647106776193, -1016.2116244340472],[-0.008522647106776138, 1.005366442807312, -1293.387118453363], [0.0, 0.0, 1.0]]
sensor.declination = 15.5


f = open("data.dat", "w")
def calculate_correct_bearing(currentbearing):
    newbearing = currentbearing+50
    if (type(currentbearing) != float):
        raise TypeError("Only floats are supported as arguments")
    else:
        
        newbearing = currentbearing+50
        
        if newbearing >= 360:
            newbearing = newbearing-360
        
        elif newbearing < 0:
            newbearing += 360 
    return newbearing


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

starttime = time.time()
print(atTarget((lat1,long1), (cur_lat, cur_long))) 
while atTarget((lat1,long1), (cur_lat, cur_long)) == False:
#for x in range(0,10):
    m = sensor.get_magnet()
    report = gpsd.next()
    if report['class'] == 'TPV':    
        heading = sensor.get_bearing()
        adjustedheading = calculate_correct_bearing(heading)
        print(adjustedheading, heading)
        print(adjustedheading)
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))
        projectedHeading = calculate_initial_compass_bearing((cur_lat,cur_long), (lat1, long1))
        necessarychange = projectedHeading-adjustedheading
        print(projectedHeading, adjustedheading, necessarychange)
        f.write(str(round(starttime - time.time(), 3)))
        f.write(" seconds into testing.")
        #print(projectedHeading)
        #print(heading)
        #print(necessarychange)      
        if necessarychange >= 10:
            print("goLeft()")
            f.write("We need to turn left. We need to be going at" + str(projectedHeading) + ", our current heading is" + str(adjustedheading) + ", and therefore the change we need to make is more than 10 degrees -" + str(necessarychange)+"\n")
            #f.write("text/n")
        elif necessarychange <= -10:
            print("goRight()")
            f.write("We need to turn right. We need to be going at" + str(projectedHeading) + ", our current heading is" + str(adjustedheading) + ", and therefore the change we need to make is more than 10 degrees -" + str(necessarychange)+"\n") 
            #f.write(" text/n")
        else:
            print("goStraight()")
            f.write("We should be going straight. We need to be going at" + str(projectedHeading) + ", our current heading is" + str(adjustedheading) + ", and therefore the change we need to make is less than 10 degrees -" + str(necessarychange)+"\n") 
            #f.write("text/n")
        time.sleep(.1)
        #stop()
        time.sleep(.1)
f.close()

