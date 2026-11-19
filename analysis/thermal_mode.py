import numpy as np
import matplotlib.pyplot as plt

# Lumped model: m*cp*dT/dt = I^2*R - h*A*(T - T_amb)
m_cp = 200.0      # J/K (thermal mass)
R = 0.05          # ohm
hA = 0.8          # W/K
T_amb = 25.0
dt = 1.0

def simulate(current, seconds=600):
    T = [T_amb]
    for _ in range(seconds):
        heat_in = current**2 * R
        heat_out = hA * (T[-1] - T_amb)
        T.append(T[-1] + (heat_in - heat_out) / m_cp * dt)
    return T

for I in (10, 20, 30):
    plt.plot(simulate(I), label=f"{I} A")
plt.axhline(60, ls="--", color="orange"); plt.axhline(75, ls="--", color="red")
plt.xlabel("Time (s)"); plt.ylabel("Temperature (°C)")
plt.legend(); plt.title("Analytical thermal model"); plt.show()
