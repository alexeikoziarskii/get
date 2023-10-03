import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
leds = [2, 3, 4, 17, 27, 22, 10, 9]
GPIO.setup(leds, GPIO.OUT, initial = 0)

powers = [128, 64, 32, 16, 8, 4, 2, 0]

levels = 2**len(dac)
comp = 14
troyka = 13
maxVoltage = 3.3

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
        '''for i in range(len(powers) - 1):
            if value <= powers[i] and value >= powers[i + 1]:
                GPIO.output(leds, dec2bin(powers[i] - 1))
            if value == 0: GPIO.output(leds, 0)'''
        value = dec2bin(value)
        for x in value:
            if x != 0:
                for i in range(value.index(x)+1, 8):
                    if value[i] == 0: value[i] = 1
                break
        GPIO.output(leds, value)

except KeyboardInterrupt:
    print("the program was stopped")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup(dac)
    




