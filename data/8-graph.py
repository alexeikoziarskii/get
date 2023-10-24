from matplotlib import pyplot as plt
import numpy as np
from textwrap import wrap
import matplotlib.ticker as ticker

with open('settings.txt', 'r') as f:
    settings = [float(i) for i in f.read().split('\n')]

data = np.loadtxt('data.txt', dtype = int) * settings[1]
time = np.array([i * settings[0] for i in range(data.size)])

fig, ax = plt.subplots(figsize = (16, 10), dpi = 200)
plt.xlim(0, 12.5)
plt.ylim(0, 2.8)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))

ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

ax.set_title('\n'.join(wrap('Процесс зарядки и разрядки конденстатора в RC цепи', 60)), loc = 'center')

ax.grid(which = 'major', color = 'k')
ax.minorticks_on()
ax.grid(which = 'minor', color = 'grey', linestyle = ':')

ax.set_xlabel('t, seconds')
ax.set_ylabel('U, volts')

ax.plot(time, data, c = 'black', linewidth = 1, label = 'U(t)')
ax.legend(shadow = False, loc = 'upper right', fontsize = 10)
plt.text(8, 1.7, 'время зарядки(с): ' + str(time[np.argmax(data)]))
plt.text(8, 1.5, 'время разрядки(с): ' + str( np.max(time) - time[np.argmax(data)]))
ax.scatter(time[0:data.size:20], data[0:data.size:20], marker = 'o', c = 'blue', s = 10)

fig.savefig('graph.png')
fig.savefig('graph.svg')
plt.show() 
