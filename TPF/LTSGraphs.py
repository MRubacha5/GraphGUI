import ltspice as lts
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#LTSPICE FILE
ltspicePath1 = "C:/Users/mgvir/OneDrive/Documentos/ITBA/2025/TC1/TPF/LTSpice_raw/PCB/SegundoOrden.raw"

l1 = lts.Ltspice(ltspicePath1)
l1.parse()

frecuency = l1.get_frequency()
V_out = l1.get_data('V(N004)')
V_in = l1.get_data('V(n006)')

H = V_out/V_in

modulo = 20*np.log10(np.abs(H))
fase = np.angle(H, deg=True)


#CSV FILE
filePathFase = "C:/Users/mgvir/Downloads/TONKI_CON_POTE_MAXIMO.csv"
filePathMag = "C:/Users/mgvir/Downloads/TONKI_CON_POTE_MAXIMO.csv"

dataFrameMag = pd.read_csv(filePathMag)
dataFrameFase = pd.read_csv(filePathFase)

X = dataFrameMag.iloc[:, 0].values
Ymag = dataFrameMag.iloc[:, 2].values
Yfase = dataFrameFase.iloc[:, 3].values

#Graph options

bode = True
bodeMode = "fase"

fig, ax1 = plt.subplots()

if bode:
    ax1.set_xlabel("Frecuencia [Hz]")
    ax1.set_xscale("log")

    if bodeMode == "mag":
        ax1.plot(frecuency, modulo, label="Modulo simulado")
        ax1.plot(X, Ymag, label="Modulo experimental")
        ax1.set_ylabel("Ganancia [dB]")
        ax1.axhline(-3, linestyle='--', color='gray', linewidth=1)
        ax1.annotate(
            "-3 dB",
            xy=(ax1.get_xlim()[0], -3),
            xytext=(-40, 0),
            textcoords='offset points',
            ha='right', va='center',
            arrowprops=dict(arrowstyle='->', color='gray')
        )

        # 2) Busco cruces de Ymag con -3 dB
        #    Signos de (Ymag + 3) cambian al cruzar -3.
        signs = np.sign(Ymag + 3)
        zero_crossings = np.where(np.diff(signs) != 0)[0]

        for idx in zero_crossings:
            # puntos alrededor del cruce
            x1, y1 = X[idx],     Ymag[idx]
            x2, y2 = X[idx + 1], Ymag[idx + 1]
            # interp. lineal para y = -3
            if (y2 - y1) != 0:
                x_cut = x1 + ( -3 - y1 ) * (x2 - x1) / (y2 - y1)
            else:
                x_cut = x1
            # 3) Marcador y línea vertical
            ax1.plot(x_cut, -3, marker='o', color='red', markersize=6,
                     label="-3 dB" if idx == zero_crossings[0] else None)
            ax1.axvline(x_cut, linestyle='--', color='red', linewidth=1)
            ax1.annotate(
                f"{x_cut:.2f} Hz",
                xy=(x_cut, ax1.get_ylim()[0]),
                xytext=(0, -30),
                textcoords='offset points',
                ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color='red')
            )


        
    else:
        ax1.plot(frecuency, fase, label="Fase simulada")
        ax1.plot(X, Yfase, label="Fase experimental")
        ax1.set_ylabel("Fase")
    
    ax1.grid(True)
    ax1.legend()

plt.show()