import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta, datetime
import matplotlib.dates as mdates

delta_t = 1/24
t = np.arange(0, 365, delta_t)
start_date = datetime(2026, 1, 1)   # any old year
dates = [start_date + timedelta(days=float(dt)) for dt in t]

B = np.repeat(57,len(t))
S = 33 * -np.cos(t * 2 * 3.14159 / (365))
D = 13 * np.sin(t * 2 * 3.14159 / (1))
N = np.random.normal(0,5,len(t))

N2 = np.empty(len(t))
N2[0] = 0

for i in range(1,len(t)):
    N2[i] = .97 * N2[i-1] + N[i]
T = B + S + D + N2

fig, axs = plt.subplots(nrows=2, figsize=(13,8))
ax = axs[0]
ax.plot(dates,B,color="black",label="baseline")
ax.plot(dates,S,color="green",label="seasonal")
ax.plot(dates,D,color="red", label="daily")
ax.plot(dates,N,color="orange", label="noise")
ax.plot(dates,T,color="brown", linewidth=2, label="temperature")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.legend()

ax = axs[1]
ax.plot(t, N, color="blue", label="noise")
ax.plot(t, N2, color="red", label="cumulative noise")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.legend()

fig.savefig("temp_model.svg")
