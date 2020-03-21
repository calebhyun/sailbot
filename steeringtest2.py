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


stop()
for x in range(0,50):
    goRight()
    time.sleep(0.5)
    goStraight()
    time.sleep(0.5)
    goLeft()
    time.sleep(0.5)
    goStraight()
