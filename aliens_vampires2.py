import matplotlib.pyplot as plt
import numpy as np

# Add limited human population, and model logistic growth.

start_t = 1940     # years
end_t = 2000       # years
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
aggressiveness = 200_000   # (abd/year)/year
bloodthirstiness = .2   # (vampires/year)/vampire


# The "stock" for alien abductees. The value of A for any index i is the
# total number of people aboard spaceships at that time.
A = np.zeros(len(t))      # abductees
A[0] = 0                  # initial condition: no abductions at the start

# The "stock" for vampires. The value of V for any index i is the total number
# of vampires at that time.
V = np.zeros(len(t))      # vampires
V[0] = 1                  # initial condition: one lonely vampire at the start

world_pop = 8_000_000_000 # individuals

H = np.zeros(len(t))      # humans
H[0] = world_pop          # start at current world population

fertility_rate = 0.05     # (babies/year)/person

for i in range(1,len(t)):

    # Compute the "logistic factor," a number from 0 (no inhibitions on growth)
    # to 1 (growth completely stopped). The "world_pop" here is also called the
    # carrying capacity.
    logistic_factor = H[i-1]/world_pop

    # Compute the values of the flows.
    abductions = aggressiveness * (itot(i)-start_t) * logistic_factor # abd/yr
    bitings = bloodthirstiness * V[i-1] * logistic_factor   # vamps/year
    births = fertility_rate * H[i-1]  # babies/year

    # Compute the primes.
    A_prime = abductions  # individuals/year
    V_prime = bitings   # individuals/year
    H_prime = -abductions - bitings + births  # individuals/year

    # Compute the next stock values.
    A[i] = A[i-1] + A_prime * delta_t
    V[i] = V[i-1] + V_prime * delta_t
    H[i] = H[i-1] + H_prime * delta_t


fig, ax = plt.subplots()
ax.plot(t, A, color="green", label="alien abductions")
ax.plot(t, V, color="red", label="vampires")
ax.plot(t, H, color="black", linestyle="dotted", label="humans")
fig.legend()
