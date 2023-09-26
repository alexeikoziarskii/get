import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
    
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
num = 0
try:
    while(True):
        s = input(num) 
        if(s == 'q'):
            break
        if not s.isdigit():
            print("введено не число")
            continue
        num = int(s)
        if(num < 0 or num > 255):
            print("число не умещается в разрядную сетку 8-бит")
            continue
        
        GPIO.output(dac, decimal2binary(num))
        print(3.3 / 256 * num)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
