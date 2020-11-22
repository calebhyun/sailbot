from time import sleep
from gps import *
import time
import RPi.GPIO as GPIO
import threading
import datetime
dt = datetime.datetime.today()
import magnetometer
import pygame, sys
import pygame.locals


'''pygame.init()
BLACK = (0,0,0)
WIDTH = 100
HEIGHT = 100
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

windowSurface.fill(BLACK)'''

#Things that are off:
#gps shifts slightly throughout (creating projected heading change of <20)
#compass bearing is a bit off (<15)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(38, GPIO.HIGH)

tolerancelat = .00005
tolerancelong = .00005

def goLeft():
    print("LEFT")
    GPIO.output(8, GPIO.HIGH)
    
    #GPIO.output(32, GPIO.LOW)
    #GPIO.output(36, GPIO.HIGH)
def goRight():
    print("RIGHT")
    GPIO.output(12, GPIO.HIGH)

    #GPIO.output(32, GPIO.HIGH)
    #GPIO.output(36, GPIO.LOW)
def goStraight():
    print("STRAIGHT")
    GPIO.output(10, GPIO.HIGH)

    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.HIGH)

def goForwards():
    #GPIO.output(38, GPIO.LOW)
    print("\n")
def stop():
    GPIO.output(38, GPIO.HIGH)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

used = False

def atTarget(pointA, pointB):
    if abs(pointA[0]-pointB[0]) < tolerancelat and abs(pointA[1]-pointB[1]) < tolerancelong:
        return True
    else:
        return False

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

def steering():
    global used, cur_long, cur_lat
    if used!=True:
        print("being used")
        used = True
        report = gpsd.next() #
        if report['class'] == 'TPV':
            cur_lat = getattr(report,'lat',0.0)
            cur_long = getattr(report,'lon',0.0)
            
            projected_bearing = calculate_initial_compass_bearing((cur_lat, cur_long), (lat1, long1))
            
            
            print(cur_lat, ", ", cur_long,"\t")
            heading = magnetometer.get_heading()

            print("bearing: ", heading, ",", "projected_bearing: ", projected_bearing)
            
            necessary_change = projected_bearing - heading
            	
            if necessary_change <= -180:
                necessary_change += 360
                
            elif necessary_change >= 180:
                necessary_change -= 360

            print("necessary change: ", necessary_change)
            #print("necessarychange changed")
            
            m = abs(necessary_change / 50);
            if necessary_change > 5:
                goRight()
                time.sleep(.2)
                goStraight()
            elif necessary_change < -5:
                goLeft()
                time.sleep(.2)
                goStraight()
            else:
                goStraight()
        #print("steering done")
        used = False

lat1 = 0.00029 #47.34211
long1 = -0.00019 #-122.32705

report = gpsd.next()
while report['class'] != 'TPV':
    report = gpsd.next()
    if report['class'] == 'TPV':
        #SWITCHED AROUND FOR TESTING PURPOSES
        cur_long = float(getattr(report,'lon',0.0))
        cur_lat = float(getattr(report,'lat',0.0))
c = open("coordinates-nautilus-jarvis.dat", "r")
coordinates_array=[]
coords = c.readline()
while coords:
    coordinates_array.append(coords.split())
    coords = c.readline()
num_of_coordinates = len(coordinates_array)

for y in range(0, num_of_coordinates):
    both_coordinates = coordinates_array[y]
    print("point \#", y+1, "coordinates:", both_coordinates)
    time.sleep(3)
    print("!\n!\n!\n!\n!\n")
    #Switched these
    lat1 = float(both_coordinates[1])
    long1 = float(both_coordinates[0])
    while atTarget((cur_lat, cur_long), (lat1, long1)) == False:
        x = threading.Thread(target= steering, args = ())
        x.start()
        
        #print("waypoint:", lat1, long1, " current position:", cur_lat, cur_long)
        
        
        '''for event1 in pygame.event.get():
            if event1.key == pygame.K_p: # replace the 'p' to whatever key you wanted to be pressed
                 print("You pressed p!") #Do what you want to here
            if event1.type == pygame.locals.QUIT:
                 pygame.quit()
                 sys.exit()'''
        
        goForwards()
        time.sleep(.1)
        stop()
        time.sleep(.2)
                  
                  
                  

