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
    
def adc(val):
    signal = dec2bin(val)
    GPIO.output(dac, signal)
    return signal
try:
    while True:
        for value in range(256):
            signal = adc(value)
            time.sleep(0.001)
            voltage = value / levels * maxVoltage
            comparVal = GPIO.input(comp)
            if comparVal == 1:
                print("ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
                break
except KeyboardInterrupt:
    print("the program was stopped")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    

