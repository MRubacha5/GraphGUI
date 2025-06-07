import ltspice as lts
import numpy as np
import matplotlib.pyplot as plt

path = "./SpiceThings/InterruptorSeCierra.raw"

l = lts.Ltspice(path)
l.parse()

time = l.get_time() * 1e6
V_0 = l.get_data('V(n002)')
V_l = l.get_data('V(n003)')
I_c = l.get_data('I(C1)')

plt.plot(time, V_0)
#plt.plot(time, I_c)
plt.xlabel("Time [us]")
plt.ylabel("Voltage [V]")
plt.xscale("linear")
plt.grid(True)
plt.show()