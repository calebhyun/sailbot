import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)


for x in range(0,100):
     GPIO.output(32, GPIO.HIGH)
     time.sleep(.1)
     GPIO.output(32, GPIO.LOW)
     time.sleep(.1)
