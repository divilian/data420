import numpy as np
import matplotlib.pyplot as plt

delta_t = 1
t = np.arange(0, 15, delta_t)

U = np.empty(len(t))
U[0] = 0
M = np.empty(len(t))
M[0] = 0
W = np.empty(len(t))
W[0] = 0

for i in range(1, len(t)):
    U_prime = 30
    M_prime = 10 * t[i]
    W_prime = 10 * t[i] * (1 - W[i-1]/200)

    U[i] = U[i-1] + U_prime * delta_t
    M[i] = M[i-1] + M_prime * delta_t
    W[i] = W[i-1] + W_prime * delta_t

fig, ax = plt.subplots()
ax.plot(t, U, color="purple", linestyle="dotted", label="U")
ax.plot(t, M, color="orange", linestyle="solid", label="M")
ax.plot(t, W, color="blue", linestyle="dashed", label="W")
fig.legend()
