import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

levels = 2**len(dac)
comp = 14
troyka = 13
maxVoltage = 3.3


GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = 1)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
    
def adc():
    tmp_value = 0
    total_value = 0
    for i in range(1, 8):
        pow2 = 2**(8 - i)
        tmp_value = total_value + pow2
        signal = dec2bin(tmp_value)
        GPIO.output(dac, signal)
        time.sleep(0.001)
        compValue = GPIO.input(comp)
        if compValue == 0:
            total_value = total_value + pow2
    return total_value
try:
    while True:
        value = adc()
        voltage = value / levels * maxVoltage
        print("value = ", value, "voltage = ", voltage)


except KeyboardInterrupt:
    print("the program was stopped")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    


