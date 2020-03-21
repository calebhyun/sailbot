import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(32, GPIO.OUT)
#GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)

for x in range(20):
    #print("LEFT")
    #GPIO.output(32, GPIO.HIGH)
    #GPIO.output(36, GPIO.LOW)
    #time.sleep(1)
    print("STRAIGHT")
    #GPIO.output(32, GPIO.HIGH)
    GPIO.output(38, GPIO.HIGH)
    time.sleep(1)    
    GPIO.output(38, GPIO.LOW)
    time.sleep(1)    

#print("RIGHT")
    #GPIO.output(32, GPIO.LOW)
    #GPIO.output(36, GPIO.HIGH)    
    #time.sleep(1)
GPIO.cleanup()

