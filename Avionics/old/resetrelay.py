import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import RPi.GPIO as GPIO


GPIO.setup(21, GPIO.OUT)
#GPIO.output(32, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
print("worked")
while 1:
    print("yo")
    #GPIO.output(32, 0)
    GPIO.output(21, 0)
    time.sleep(1)