import matplotlib.pyplot as plt
import numpy as np

delta_x = 1/365                             # years
x = np.arange(1880,2000,delta_x)            # years

banks = 4                                   # banks
deposits_per_bank = 7500                    # $/bank
birth_factor = .01                          # (individuals/individual)/year
murder_factor = .01                         # (murders/year)/outlaw
arrest_factor = .008                        # (arrests/year)/(deputy*outlaw)
recruit_factor = .005                       # (recruits/excessOutlaws)
maturity_factor = 1/18                      # unitless
funds_in_city = banks * deposits_per_bank   # $
life_of_crime_temptation = 10e5             # dollar*years

adults = np.empty(len(x))                   # individuals
adults[0] = 1500
children = np.empty(len(x))                 # individuals
children[0] = 322
outlaws = np.empty(len(x))                  # individuals
outlaws[0] = 800
deputies = np.empty(len(x))                 # individuals
deputies[0] = 2

for i in range(1,len(x)):
    birth_rate = adults[i-1] * birth_factor
    graduate_rate = children[i-1] * maturity_factor
    murder_rate = outlaws[i-1] * murder_factor
    arrest_rate = (deputies[i-1] * outlaws[i-1]) * arrest_factor
    new_villain_rate = adults[i-1] * funds_in_city / life_of_crime_temptation
    recruit_rate = max(0,outlaws[i-1] - deputies[i-1]) * recruit_factor 

    children_prime = birth_rate - graduate_rate
    children[i] = children[i-1] + children_prime * delta_x

    adults_prime = graduate_rate - murder_rate
    adults[i] = adults[i-1] + adults_prime * delta_x

    outlaws_prime = new_villain_rate - arrest_rate
    outlaws[i] = outlaws[i-1] + outlaws_prime * delta_x

    deputies_prime = recruit_rate
    deputies[i] = deputies[i-1] + deputies_prime * delta_x

plt.plot(x,children,label="children",color="blue")
plt.plot(x,adults,label="adults",color="green")
plt.plot(x,outlaws,label="outlaws",color="purple")
plt.plot(x,deputies,label="deputies",color="red")
plt.legend()
