
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Create an array of temperature points that kinda sorta mimics what the earth
# actually does.
def get_outside_temp_vec(
    delta_t:float,  # days
    num_days:int,
    baseline:float,
    daily_fluc:float,
    seasonal_fluc:float,
    noise:float
) -> np.ndarray:

    t = np.arange(0, num_days, delta_t)                                # days

    baseline = np.repeat(baseline,len(t))                              # degF
    seasonal = seasonal_fluc * -np.cos(t * 2 * 3.14159 / (365))        # degF
    daily = daily_fluc * np.sin(t * 2 * 3.14159 / (1))                 # degF
    noise = np.random.normal(0,noise,len(t))                           # degF
    return baseline + seasonal + daily + noise


# Put the whole simulation in a function, so we can parameter sweep it.
def run_sim(
    thermostat,                  # our desired indoor temp (degF)
    baseline,                    # overall avg outdoor temp (degF)
    daily_fluc,                  # +/- due to daily effects (degF)
    seasonal_fluc,               # +/- due to seasonal effects (degF)
    noise,                       # +/- due to random effects (degF)
    insulation_loss_rate = .3,   # how fast we lose heat (degF/hr)/degF
    furnace_power = 16           # how fast our furnace heats degF/hr
):
    num_days = 365

    delta_t = 1/60                # hrs
    t = np.arange(0,24*num_days,delta_t)   # hrs

    outside_temp = get_outside_temp_vec(
        delta_t / 24,
        num_days,
        baseline,
        daily_fluc,
        seasonal_fluc,
        noise,
    )

    T = np.empty(len(t))          # degF
    T[0] = 67                     # degF

    furnace_on = np.empty(len(t), dtype=bool)
    furnace_on[0] = True

    hysteresis = 5 # degF

    for i in range(1, len(t)):

        if T[i-1] < thermostat - hysteresis:
            furnace_on[i] = True
        elif T[i-1] > thermostat + hysteresis:
            furnace_on[i] = False
        else:
            furnace_on[i] = furnace_on[i-1]
        
        # ...compute flows...
        if furnace_on[i]:
            heating = furnace_power
        else:
            heating = 0

        leakage = insulation_loss_rate * (T[i-1] - outside_temp[i-1])

        T_prime = heating - leakage

        T[i] = T[i-1] + T_prime * delta_t

    # Return our one lonely d.v. (dependent variable), throwing away all other
    # details of this simulation run.
    return furnace_on.sum()/len(furnace_on)*100

# Code for plotting a single simulation in detail (now commented out for our
# parameter sweep.)
#plt.plot(t,T,color="orange",label="inside temp")
#plt.plot(t,furnace_on * 10,color="gray",linewidth=2,label="furnace on/off")
#plt.plot(t,outside_temp, color="blue", linestyle="dashed",
#    label="outside temp")
#plt.axhline(y=thermostat, color="brown", linestyle="dotted", label="thermostat")
#plt.xlabel("hours")
#plt.ylabel("deg F")
#plt.ylim(top=100)
#plt.legend()
#plt.show()

# Parameter sweep: run the simulation many times, for varying values of our
# i.v. (independent variable), capturing and recording the d.v. for each one.
thermostat_values = np.arange(0,200,5)
percentage_furnace_ons = np.empty(len(thermostat_values))
for i in tqdm(list(range(len(thermostat_values)))):
    percentage_furnace_ons[i] = run_sim(
        thermostat_values[i],
        baseline=57,
        daily_fluc=16,
        seasonal_fluc=30,
        noise=2,
        insulation_loss_rate=.3,
        furnace_power=16,
    )

fig, ax = plt.subplots()
ax.plot(thermostat_values, percentage_furnace_ons)
ax.set_xlabel(r'Thermostat ($^\circ$F)')
ax.set_ylabel('Percent furnace on (%)')
