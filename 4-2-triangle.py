import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
    
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)

try:
    period_val = int(input())
    num_of_periods = int(input())
    j = 0
    for i in range(num_of_periods):
        while(j < 255):
            GPIO.output(dac, dec2bin(int(j)))
            print(3.3 / 256 * int(i))
            j = j + 1
            time.sleep(period_val / 512)
        while(j):
            GPIO.output(dac, dec2bin(int(j)))
            print(3.3 / 256 * int(i))
            j = j - 1
            time.sleep(period_val / 512)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()