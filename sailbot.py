import math
import py_qmc5883l
from time import sleep
from gps import *
import time
import RPi.GPIO as GPIO
import time
import datetime
dt = datetime.datetime.today()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
#Tahlequah Vashon Island
#Tahlequah Vashon Island
#long1 = -122.516422
#lat1 = 47.355398
long1 = -122.314953
lat1 = 47.335799
tolerancelat = .00001
toleranellong = .00001
#houselat = 47.342257833 	
#houselong = -122.326749667 	
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
sensor = py_qmc5883l.QMC5883L()
sensor.calibration = [[1.00579223e+00, -9.69727879e-03, -8.50240184e+02],  [-9.69727879e-03, 1.01623506e+00, -1.77743179e+03],  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
sensor.declination = 15.5

f = open("data.dat", "w")
def calculate_correct_bearing(currentbearing):
    newbearing = currentbearing+50
    if (type(currentbearing) != float):
        raise TypeError("Only floats are supported as arguments")
    else:
        
        newbearing = 360-currentbearing-45 
        
        if newbearing >= 360:
            newbearing = newbearing-360
        
        elif newbearing < 0:
            newbearing += 360 
    return newbearing

g = open("data/test-coordinates"+dt.isoformat()+".dat", "w+")

def goLeft():
    print("LEFT")
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
def goRight():
    print("RIGHT")
    GPIO.output(32, GPIO.LOW)
    GPIO.output(36, GPIO.HIGH)
def goStraight():
    print("STRAIGHT")
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.HIGH)
def goForwards():
    GPIO.output(38, GPIO.LOW)
    print("forwards")
def stop():
    GPIO.output(38, GPIO.HIGH)

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

def atTarget(pointA, pointB):
    if abs(pointA[0]-pointB[0]) < tolerancelat and abs(pointA[1]-pointB[1]) < tolerancelong:
        return True
    else:
        return False

m = sensor.get_magnet()
report = gpsd.next()
while report['class'] != 'TPV':
    report = gpsd.next()
    if report['class'] == 'TPV':
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))
heading = 0
starttime = time.time()
while atTarget((lat1,long1), (cur_lat, cur_long)) == False:
    try:
        m = sensor.get_magnet()
    except:
        print("error magnet")
        continue
    report = gpsd.next()
    if report['class'] == 'TPV':    
        goForwards()
        try:
            heading = sensor.get_bearing()
        except:
            print("problem with bearing")
            continue
        
        adjustedheading = calculate_correct_bearing(heading)
        
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))
        
        projectedHeading = calculate_initial_compass_bearing((cur_lat,cur_long), (lat1, long1))
        necessarychange = projectedHeading-adjustedheading
        print(projectedHeading, adjustedheading, necessarychange)
        
        f.write(str(round(starttime - time.time(), 3)))
        f.write(" seconds into testing.")
        g.write(str(cur_long) + ", " + str(cur_lat))
        if necessarychange >= 10:
            goLeft()
            f.write("We need to turn left. We need to be going at " + str(projectedHeading) + ", our current heading is " + str(heading) + ", and therefore the change we need to make is more than 10 degrees, or " + str(necessarychange)+"\n")
            #f.write("text/n")
        elif necessarychange <= -10:
            goRight()
            f.write("We need to turn right. We need to be going at " + str(projectedHeading) + ", our current heading is " + str(heading) + ", and therefore the change we need to make is more than 10 degrees, or " + str(necessarychange)+"\n") 
            #f.write(" text/n")
        else:
            goStraight()
            f.write("We should be going straight. We need to be going at " + str(projectedHeading) + ", our current heading is " + str(heading) + ", and therefore the change we need to make is less than 10 degrees, or " + str(necessarychange)+"\n") 
            #f.write("text/n")
        time.sleep(.2)
        stop()
        time.sleep(.1)
stop()
f.close()


