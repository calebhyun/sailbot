import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
#GPIO.output(32, GPIO.HIGH)
#time.sleep(5)
GPIO.output(32, GPIO.LOW)
GPIO.cleanup()
