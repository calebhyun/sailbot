from time import sleep
from gps import *
import time
import RPi.GPIO as GPIO
import threading
import datetime
dt = datetime.datetime.today()
import magnetometer
import pygame, sys
from pygame.locals import *


pygame.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0, 255)
RED = (255, 0, 0)

SCREENWIDTH = 1000
SCREENHEIGHT = 600
WIDTHMIDPOINT = SCREENWIDTH/2
HEIGHTMIDPOINT = SCREENHEIGHT/2

windowSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)

windowSurface.fill(BLACK)

DISPLAYSURF = pygame.display.set_mode(((SCREENWIDTH, SCREENHEIGHT)))

fontObj = pygame.font.SysFont('Times New Roman', 16)

def writeText(text, position, color = WHITE):
    global fontObj, DISPLAYSURF
        
    txtSurf = fontObj.render(text, True, color)
    txtRect = txtSurf.get_rect()
    txtRect.topleft = (position)

    DISPLAYSURF.blit(txtSurf, txtRect)


#########################################################


GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(38, GPIO.HIGH)

tolerancelat = .00003
tolerancelong = .00003

def goLeft():
    GPIO.output(8, GPIO.HIGH)
    
    #GPIO.output(32, GPIO.LOW)
    #GPIO.output(36, GPIO.HIGH)
def goRight():
    GPIO.output(12, GPIO.HIGH)

    #GPIO.output(32, GPIO.HIGH)
    #GPIO.output(36, GPIO.LOW)
def goStraight():
    GPIO.output(10, GPIO.HIGH)

    GPIO.output(32, GPIO.HIGH)
    GPIO.output(36, GPIO.HIGH)

def goForwards():
    #GPIO.output(38, GPIO.LOW)
    filler = 0

def stop():
    GPIO.output(38, GPIO.HIGH)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)

######################################################

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

    compass_bearing = (initial_bearing +360) % 360
    return compass_bearing

def steering():
    global used, cur_long, cur_lat, heading, necessary_change, projected_bearing, position
    if used!=True:
        used = True
        report = gpsd.next() #
        if report['class'] == 'TPV':
            cur_lat = getattr(report,'lat',0.0)
            cur_long = getattr(report,'lon',0.0)
            
            projected_bearing = calculate_initial_compass_bearing((cur_lat, cur_long), (lat1, long1))
            
            heading = magnetometer.get_heading()
            print(heading)
            
            necessary_change = projected_bearing - heading
            	
            if necessary_change <= -180:
                necessary_change += 360
                
            elif necessary_change >= 180:
                necessary_change -= 360
            
            m = abs(necessary_change / 50);
            if necessary_change > 5:
                goRight()
                position = "Right"
                time.sleep(.2)
                goStraight()
            elif necessary_change < -5:
                goLeft()
                position = "Left"
                time.sleep(.2)
                goStraight()
            else:
                goStraight()
                position = "Straight"
        used = False

lat1 = 0.0 #47.34211
long1 = 0.0 #-122.32705
heading = 0.0
projected_bearing = 0.0
necessary_change = 0.0
position = "Straight"

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
    for z in range(0, y):
        GPIO.output(8, GPIO.HIGH)
        GPIO.output(10, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        time.sleep(.5)

    time.sleep(3)
    #Switched these
    lat1 = float(both_coordinates[1])
    long1 = float(both_coordinates[0])
    while atTarget((cur_lat, cur_long), (lat1, long1)) == False:
        x = threading.Thread(target = steering, args = ())
        x.start()
        
        goForwards()
        time.sleep(.1)
        stop()
        time.sleep(.2)
                  
        
        DISPLAYSURF.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == QUIT: 
                    pygame.quit()
                    sys.exit
        
        pygame.draw.line(DISPLAYSURF, RED, (WIDTHMIDPOINT, 0), (WIDTHMIDPOINT, SCREENHEIGHT), 3)
        pygame.draw.line(DISPLAYSURF, RED, (0, HEIGHTMIDPOINT), (WIDTHMIDPOINT, HEIGHTMIDPOINT), 3)       
        
        writeText("Variables: ", (WIDTHMIDPOINT + 10, 5))
        
        writeText("GPS ", (WIDTHMIDPOINT + 20, 25))
        writeText("Going to waypoint: " + str(y + 1), (WIDTHMIDPOINT + 20, 65))
        writeText("Waypoint Latitude: " + str(lat1) + ", Waypoint Longitude" + str(long1), (WIDTHMIDPOINT + 20, 85))
        writeText("Latitude: " + str(cur_lat) + ", Longitude: " + str(cur_long), (WIDTHMIDPOINT + 20, 45))
        #writeText("Latitude Tolerance: " + str(tolerancelat) + ", Longitude Tolerance: " + str(tolerancelong), (WIDTHMIDPOINT + 20, 105))
        writeText("Latitude Tolerance: .00003, Longitude Tolerance: .00003", (WIDTHMIDPOINT + 20, 105))
        writeText("Lat from Waypoint: " + str(round(cur_lat - lat1, 8)), (WIDTHMIDPOINT + 20, 125))
        writeText("Long from Waypoint: " + str(round(cur_long - long1, 8)), (WIDTHMIDPOINT + 20, 145))
        writeText("AtTarget ==  " + str(atTarget((cur_lat, cur_long), (lat1, long1))), (WIDTHMIDPOINT + 20, 165))
        
        writeText("Compass: ", (WIDTHMIDPOINT + 20, 205))
        writeText("Current Heading: " + str(round(heading, 1)), (WIDTHMIDPOINT + 20, 225))
        writeText("Desired Heading: " + str(round(projected_bearing, 1)), (WIDTHMIDPOINT + 20, 245))
        writeText("Necessary Change: " + str(round(necessary_change, 1)), (WIDTHMIDPOINT + 20, 265))
        writeText("Range of Straight: -5 < x < 5", (WIDTHMIDPOINT + 20, 285))
        
        writeText("Car: ", (WIDTHMIDPOINT + 20, 325))
        writeText("Turning Position: " + position, (WIDTHMIDPOINT + 20, 345))
        #writeText("Forwards Interval: " + position, (WIDTHMIDPOINT + 20, 345))
        #writeText("Turning Position: " + position, (WIDTHMIDPOINT + 20, 365))
    
        pygame.display.update()        

                  
                  

