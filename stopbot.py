import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.output(32, GPIO.HIGH)
GPIO.output(36, GPIO.HIGH)
GPIO.output(38, GPIO.HIGH)
