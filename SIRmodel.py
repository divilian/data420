
import numpy as np
import matplotlib.pyplot as plt

transmissibility = .01    # infections/contact
contact_factor = 10 #  contacts/(day*person)
mean_infected_duration = 10  # days
mortality_factor = 0    # 1/day
population = 10_000

delta_t = 1   # 1 day
t = np.arange(0, 365, delta_t)

S = np.empty(len(t))
S[0] = population - 1
I = np.empty(len(t))
I[0] = 1
R = np.empty(len(t))
R[0] = 0


for i in range(1, len(t)):

    contact_rate = contact_factor * I[i-1]   # contacts/day
    frac_susc = S[i-1] / population          # unitless

    infection = transmissibility * contact_rate * frac_susc # infections/day

    recovery_factor = 1/mean_infected_duration   # 1/days
    recovery = recovery_factor * I[i-1]

    S_prime = -infection
    I_prime = infection - recovery
    R_prime = recovery

    S[i] = S[i-1] + S_prime * delta_t
    I[i] = I[i-1] + I_prime * delta_t
    R[i] = R[i-1] + R_prime * delta_t

plt.plot(t, S, color="blue", label="susceptible")
plt.plot(t, I, color="red", label="infected")
plt.plot(t, R, color="green", label="recovered")

# "infections per person"
R_0 = contact_factor * transmissibility * mean_infected_duration


perc_inf = (R[-1] + I[-1])/population * 100
print(f"{perc_inf:.2f}% of the population got the disease.")
print(f"The R_0 for this disease was {R_0:.2f}.")
