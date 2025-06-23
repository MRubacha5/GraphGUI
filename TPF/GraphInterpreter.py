import pandas as pd
import numpy as np
import ltspice as lts
import matplotlib.pyplot as plt

filePath = "C:/Users/mgvir/Downloads/TP3Fisica.csv"

dataFrame = pd.read_csv(filePath)

X = dataFrame.iloc[:, 0].tolist()

scaleFactor = 1
displacementFactor = 0
xScale = "log"
yScale = "linear"

for cols in range(len(dataFrame.columns)-1):
    Y = dataFrame.iloc[:, cols+1].tolist()
    for i in range(len(Y)):
        Y[i] = scaleFactor * Y[i] + displacementFactor
    plt.plot(X, Y)

plt.xscale(xScale)
plt.yscale(yScale)
plt.xlabel("Time [s]")
plt.ylabel("Volts [v]")
plt.title("TITULO")

plt.show()
