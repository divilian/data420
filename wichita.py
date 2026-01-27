#!/usr/bin/env python3
'''
DATA 420 -- Numerical calculus example
Stephen Davies, University of Mary Washington, spring 2026
'''

import matplotlib.pyplot as plt
import numpy as np

# Create an array recording my speed at every hour of my family's Denver to
# Wichita road trip.
s = np.array([30,54,75,75,75,70,70,70,0,70,35])  # mph

# Later on in this example, we replaced those hardcoded speeds with randomly
# generated speeds, and we "measured" those fictitious speeds 10 times as
# often.
s = np.random.uniform(0, 100, len(s))

# Create our independent variable array. It records the real-world "meaning" of
# the time associated with each element of the array.
start_t = 9  # hours (military time)
delta_t = 1  # hours
t = np.arange(start_t, start_t + len(s) * delta_t, delta_t)  # hours

# Calc II: Integrate speed to get distance.
d = np.empty(len(s)+1)  # miles
d[0] = 1000  # miles from WC  (Initial condition)
for i in range(1,len(d)):
    d[i] = d[i-1] + s[i-1] * delta_t   # miles from West Coast


# Calc I: Differentiate the distance to get speed back. (Record this
# reconstructed speed in a new variable, s2, so we can visually confirm it's
# identical to s.)
s2 = np.empty(len(s))  # mph
for i in range(len(s2)):
    s2[i] = (d[i+1] - d[i]) / delta_t


# Plot the stuff, including both s and s2 "on top of each other" to confirm
# that our reconstructed speed is identical to the original speed. (Thus
# proving the Fundamental Theorem of Calculus: integration and differentiation
# are inverses.)
fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(13,8))
dist_ax = axs[0]
speed_ax = axs[1]

speed_ax.plot(t, s, color="red", label="speed (mph)")
speed_ax.plot(t, s2, color="purple", linewidth=5, linestyle="dotted",
    label="speed (mph)")
speed_ax.set_xlabel("time (military)")
speed_ax.set_ylabel("speed (mph)")
dist_ax.plot(t, d[:-1], color="blue", label="dist (miles) from West Coast")
dist_ax.set_ylabel("dist (miles) from West Coast")

plt.legend()
plt.show()
