import matplotlib.pyplot as plt
import numpy as np


start_t = 1940     # years
end_t = 2116       # years
delta_t = 1/12     # years
t = np.arange(start_t, end_t, delta_t)

# Given an i index into one of our stocks, return the corresponding real-world
# time.
def itot(i):
    return (i * delta_t) + start_t

# Given a real-world time, return the corresponding index into our stocks.
def ttoi(t):
    return int((t - start_t) / delta_t)


# Parameters of the simulation.
aggressiveness = 1000   # (abd/year)/year
bloodthirstiness = .1   # (vampires/year)/vampire


# The "stock" for alien abductees. The value of A for any index i is the
# total number of people aboard spaceships at that time.
A = np.zeros(len(t))    # abductees
A[0] = 0    # initial condition: no abductions at the start

# The "stock" for vampires. The value of V for any index i is the total number
# of vampires at that time.
V = np.zeros(len(t))    # vampires
V[0] = 1    # initial condition: one lonely vampire at the start

for i in range(1,len(t)):

    # Compute the values of the flows.
    abductions = aggressiveness * (itot(i) - start_t)  # abd/year
    bitings = bloodthirstiness * V[i-1]    # vamps/year

    # Compute the primes.
    A_prime = abductions
    V_prime = bitings

    # Compute the next stock values.
    A[i] = A[i-1] + A_prime * delta_t
    V[i] = V[i-1] + V_prime * delta_t


fig, ax = plt.subplots()
ax.plot(t, A, color="green")
ax.plot(t, V, color="red")

