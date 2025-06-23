import ltspice as lts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#LTSPICE FILE
ltspicePath1 = "./LTSpice_raw/Simulacion3Bode.raw"
ltspicePathCon = "C:/Users/mgvir/OneDrive/Documentos/ITBA/2025/TC1/TP4/Simulacion5ConRL.raw"
ltspicePathSin = "C:/Users/mgvir/OneDrive/Documentos/ITBA/2025/TC1/TP4/Simulacion5SinRL.raw"

l1 = lts.Ltspice(ltspicePath1)
l1.parse()

frecuency = l1.get_frequency()
V_R = l1.get_data('V(n004)')
V_C = l1.get_data('V(N001,N002)')
V_L = l1.get_data('V(N002,N003)')
V_in = l1.get_data('V(n005)')

H = V_L/V_in

modulo = 20*np.log10(np.abs(H))
fase = np.angle(H, deg=True)

lcon = lts.Ltspice(ltspicePathCon)
lcon.parse()
frecuenciaCon = lcon.get_frequency()
V_R1 = lcon.get_data('V(n002)')
V_inc = lcon.get_data('V(n003)')
modulocon = 20*np.log10(np.abs(V_R1/V_inc))
fasecon = np.angle(V_R1/V_inc, deg=True)

lsin = lts.Ltspice(ltspicePathSin)
lsin.parse()
frecuenciaSin = lsin.get_frequency()
V_R2 = lsin.get_data('V(n002)')
V_ins = lsin.get_data('V(n003)')
modulosin = 20*np.log10(np.abs(V_R2/V_ins))
fasesin = np.angle(V_R2/V_ins, deg=True)


#CSV FILE
filePathFase = "C:/Users/mgvir/Downloads/TP3Fisica.csv"
filePathMag = "C:/Users/mgvir/Downloads/TP3Fisica.csv"

dataFrameMag = pd.read_csv(filePathMag)
dataFrameFase = pd.read_csv(filePathFase)

X = dataFrameMag.iloc[:, 0].tolist()
Ymag = dataFrameMag.iloc[:, 1].tolist()
Yfase = dataFrameFase.iloc[:, 3].tolist()

#Graph options

bode = True
bodeMode = "mag"

fig, ax1 = plt.subplots()

if bode:
    octaves = [62150, 124300, 248600, 497200]
    labels = ['62.15kHz', '124.3kHz ($f_0$)', '248.6kHz', '497.2kHz']
    ax1.set_xlabel("Frecuencia [Hz]")
    ax1.set_xscale("log")

    if bodeMode == "mag":
        #ax1.plot(frecuency, modulo, label="Modulo simulado")
        ax1.plot(X, Ymag, label="Modulo experimental")
        ax1.set_ylabel("Ganancia en el capacitor [dB]")

        
    else:
        ax1.plot(frecuency, fase, label="Fase simulada")
        ax1.plot(X, Yfase, label="Fase experimental")
        ax1.set_ylabel("Fase")
    
    ax1.grid(True)
    ax1.legend()
    #ax1.set_xlim(50000, 494400)
    #ax1.minorticks_off()
    #ax1.set_xticks(octaves, labels)

plt.show()