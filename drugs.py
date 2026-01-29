import numpy as np
import matplotlib.pyplot as plt
import math

simulation_hours = 24 * 3                      # hrs (taking meds for 3 days)
delta_t = 5/60                                 # hrs
t = np.arange(0, simulation_hours, delta_t)    # hrs

# Convert simulation 'tick' number to wall clock time.
def itot(i):
    return 0 + delta_t * i

# Convert wall clock time to simulation 'tick' number.
def ttoi(t):
    return int((t - 0) / delta_t)

# A drug's half-life is how long it takes for half of the drug to be eliminated
# from your system. (We can employ "extended release" manufacturing techniques
# to increase this.)
half_life = 3.2                                # hrs
elimination_constant = math.log(2)/half_life   # 1/hr

# Your plasma volume is how much watery stuff is in your body. What matters is
# not the raw amount of drug in your system, but rather what percentage of your
# blood has that amount.
plasma_volume = 3000                           # ml (typical adult)

D = np.empty(len(t))                # ug  ("u" = "micro")
dose = 1 * 325 * 1000               # ug  take one 325 mg pill each n hrs
D[0] = dose                         # ug  start off with our first dose!
dosing_interval = 3                 # hrs (how often to take our dose)

MEC = 100  # you need at least this much of the drug for it to work  (ug/ml)
MTC = 200  # don't exceed this or you might get a rash or even die   (ug/ml)

for i in range(1,len(t)):
    # If we're exactly on a time interval boundary, take our next dose.
    if itot(i) % dosing_interval == 0:
        intake = dose / delta_t    # ug/hr
    # Otherwise, just chill and let the meds do their work.
    else:
        intake = 0

    # Compute the rate at which the drug is getting eliminated from our system
    # right at this instant.
    elimination = D[i-1] * elimination_constant   # ug/hr

    # Compute the "prime": sum of inflows minus sum of outflows.
    Dprime = intake - elimination

    # Compute the next stock value by integrating the "prime."
    D[i] = D[i-1] + Dprime * delta_t


# Now that the simulation is done, use a simple NumPy broadcast operation to
# compute the concentration (not the raw amount) of the drug in the patient's
# system at each point in time.
plasma_concentration = D / plasma_volume

# Show me what's up.
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13,8))
ax.plot(t, plasma_concentration, color="brown", label="concentration")
ax.axhline(MTC, color="red")
ax.axhline(MEC, color="green")
ax.set_xlabel("Time since dose (hours)")
ax.set_ylabel("Plasma concentration (ug/ml)")
ax.set_title("This is your brain on drugs")
ax.set_ylim(bottom=0)
fig.legend()
