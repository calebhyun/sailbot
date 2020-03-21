import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
#GPIO.output(32, GPIO.HIGH)
#time.sleep(5)
GPIO.output(38, GPIO.HIGH)
GPIO.cleanup()
