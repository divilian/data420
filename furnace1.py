
import numpy as np
import matplotlib.pyplot as plt

thermostat = 68               # degF
outside_temp = 40             # degF
insulation_loss_rate = .2     # (degF/hr)/degF
furnace_power = 6             # degF/hr

delta_x = 1/60                # hrs
x = np.arange(0,24,delta_x)   # hrs

T = np.empty(len(x))          # degF
T[0] = 67                     # degF

furnace_on = np.empty(len(x), dtype=bool)
furnace_on[0] = True

for i in range(1, len(x)):
    if not furnace_on[i-1] and T[i-1] < thermostat - 1:
        furnace_on[i] = True
    elif furnace_on[i-1] and  T[i-1] > thermostat + 1:
        furnace_on[i] = False
    else:
        furnace_on[i] = furnace_on[i-1]

    if furnace_on[i]:
        heating = furnace_power   # degF/hr
    else:
        heating = 0

    leakage = insulation_loss_rate * (T[i-1] - outside_temp)  # degF/hr

    Tprime = heating - leakage    # degF/hr
    T[i] = T[i-1] + Tprime * delta_x


plt.plot(x,T,color="orange",label="inside temp")
plt.plot(x,furnace_on * 10,color="gray",linewidth=2,label="furnace on/off")
plt.axhline(y=outside_temp, color="blue", linestyle="dashed",
    label="outside temp")
plt.axhline(y=thermostat, color="brown", linestyle="dotted", label="thermostat")
plt.xlabel("hours")
plt.ylabel("deg F")
plt.ylim(bottom=0, top=100)
plt.legend()
plt.show()

print(f"The furnace was on {furnace_on.sum()/len(furnace_on)*100:.1f}% today.")
