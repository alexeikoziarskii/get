import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)

p = GPIO.PWM(22, 1000)

duty = 0
try:
    while True:
        duty = int(input())
p.start(duty)

input()
p.stop()
finally:
    .cleanup()