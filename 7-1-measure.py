import RPi.GPIO as GPIO
import time as time
from matplotlib import pyplot

GPIO.setmode(GPIO.BCM)
leds = [2, 3, 4, 17, 27, 22, 10, 9]
GPIO.setup(leds, GPIO.OUT)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT, initial = GPIO.HIGH)

levels = 2**len(dac)
maxVoltage = 3.3
quantization_step = maxVoltage / levels
comp = 14
troyka = 13
time_list = []

GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

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
        time.sleep(0.005)
        compValue = GPIO.input(comp)
        if compValue == 0:
            total_value = total_value + pow2
    return total_value

try:
    currency = 0
    result_measure = []
    time_start = time.time()
    count = 0
    
    #зарядка конденсатора
    print('начало зарядки')
    while(currency < 205):
        currency = adc()
        time_list.append(time.time() - time_start)
        time.sleep(0)
        count += 1
        GPIO.output(leds, dec2bin(currency))
        voltage = currency / levels * maxVoltage
        result_measure.append(voltage)
        #print("voltage = ", voltage)
        
    time_of_charge = time.time()-time_start
    voltage_capacitor_max = voltage
    GPIO.output(troyka, 0)
    
    #разрядка конденсатора
    print('начало разрядки')
    while(currency > 192):
        currency = adc()
        time_list.append(time.time() - time_start)
        time.sleep(0)
        count += 1
        GPIO.output(leds, dec2bin(currency))
        voltage = currency / levels * maxVoltage
        result_measure.append(voltage)
        #print("voltage = ", voltage)
    voltage_capacitor_min = voltage
    time_of_discharge = time.time()-time_start-time_of_charge
    time_experiment = time.time()-time_start
    
    
finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
    
frequency_of_discretization = count / time_experiment

print('максимальное напряжение на конденсаторе: ')
print(voltage_capacitor_max)
print('минимальное напряжение на конденсаторе: ')
print(voltage_capacitor_min)
print('время зарядки конденсатора')
print(time_of_charge)
print('время разрядки конденсатора')
print(time_of_discharge)
print('общая продолжительность эксперимента: ')
print(time_experiment)
print('период одного измерения: ')
print(time_experiment/count)
print('средняя частота дискретизации проведенного эксперимента: ')
print(frequency_of_discretization)
print('шаг квантования АЦП: ')
print(quantization_step)

#запись данных в файл
print('запись данных')
with open('data.txt', 'w') as data:
    for i in result_measure:
        data.write(str(i) + '\n')
with open('settings.txt', 'w') as settings:
    settings.write(str(frequency_of_discretization) + '\n')
    settings.write(str(quantization_step) + '\n')
    
x = time_list
y = [i for i in result_measure]
pyplot.plot(x, y)
pyplot.xlabel('t,(sec)')
pyplot.ylabel('U, volts')
pyplot.show() 

    