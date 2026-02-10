
import numpy as np
import matplotlib.pyplot as plt

def get_outside_temp_vec(
    delta_t:float,  # days
    num_days:int,
    baseline:float,
    daily_fluc:float,
    seasonal_fluc:float,
    noise:float
) -> np.ndarray:

    t = np.arange(0, num_days, delta_t) # days (6 months, Jan 1 to Jun 30)

    baseline = np.repeat(baseline,len(t))   # degF
    seasonal = seasonal_fluc * -np.cos(t * 2 * 3.14159 / (365))
    daily = daily_fluc * np.sin(t * 2 * 3.14159 / (1))
    noise = np.random.normal(0,noise,len(t))
    return baseline + seasonal + daily + noise

thermostat = 68               # degF
num_days = 365

insulation_loss_rate = .3     # (degF/hr)/degF
furnace_power = 16             # degF/hr

delta_t = 1/60                # hrs
t = np.arange(0,24*num_days,delta_t)   # hrs

outside_temp = get_outside_temp_vec(delta_t / 24, num_days, 57, 16, 21, 2)

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

plt.plot(t,T,color="orange",label="inside temp")
plt.plot(t,furnace_on * 10,color="gray",linewidth=2,label="furnace on/off")
plt.plot(t,outside_temp, color="blue", linestyle="dashed",
    label="outside temp")
plt.axhline(y=thermostat, color="brown", linestyle="dotted", label="thermostat")
plt.xlabel("hours")
plt.ylabel("deg F")
plt.ylim(top=100)
plt.legend()
plt.show()

print(f"The furnace was on {furnace_on.sum()/len(furnace_on)*100:.1f}% today.")
