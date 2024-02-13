
import numpy as np
import matplotlib.pyplot as plt

delta_x = 1/365    # years
start_x = 1940     # year

# Given a point in time (year) return the corresponding array index (unitless).
def xtoi(x):
    return int((x - start_x) / delta_x)

# Given an array index, return the corresponding time (year).
def itox(i):
    return i * delta_x + start_x


# How aggressive are the aliens? At what rate do they abduct victims for every
# year after 1940?
aggressiveness = 1000   # (abd/year)/year

# How thirsty are the vampires? How many does each one bite, on average, in a
# year?
bloodthirstiness = .1   # (vampires/year)/vampire

# Our x-values: the precise times at which we will measure and compute the
# quantities of interest.
x = np.arange(start_x, 2124, delta_x)   # years

# Our "stock variables": one for the number of UFO-abducted victims, and one
# for the number of vampires. They are arrays, of course, because we want to
# track how many of each quantity there are *at each time period*.
A = np.empty(len(x))   # abductions
V = np.empty(len(x))   # vampires

# Set our initial conditions. When the simulation begins at the stroke of
# midnight New Year's Day 1940, there's nobody on spaceships yet, and there's
# one lonely vampire in the world.
A[0] = 0
V[0] = 1

# The main simulation loop. For each time period...
for i in range(1, len(x)):

    # ...calculate the flows...
    abduction = (itox(i) - start_x) * aggressiveness       # abd/year
    vampirization = V[i-1] * bloodthirstiness              # vamp/year

    # ...calculate the rates...
    Aprime = abduction
    Vprime = vampirization

    # ...increment the stocks.
    A[i] = A[i-1] + Aprime * delta_x                # abd
    V[i] = V[i-1] + Vprime * delta_x                # vamp


# Let's see what this bad boy looks like.
plt.plot(x, A/1e6, color="green", linestyle="dashed", label="alien abduction")
plt.plot(x, V/1e6, color="red", label="vampires")
plt.xlabel("year")
plt.ylabel("millions of abductees / vampires")
plt.legend()
plt.show()
