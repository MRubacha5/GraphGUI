import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import mplcursors
from PyQt6.QtWidgets import (

    QWidgetAction, QApplication, QGridLayout, QMainWindow, 
    QVBoxLayout, QWidget, QMessageBox, QPushButton, QLabel, QFileDialog,
    QMenu, QMenuBar
    
    )
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction
import pandas as pd
from graph_class import GraphClass
from graph_properties import GraphProperties


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #-----------WindowData----------------#

        self.setWindowTitle("GRAPHIC INTERFASE")
        self.setAcceptDrops(True)
        self.setMinimumSize(800,600)

        #-------------MENUBAR-----------------#

        self.menu_bar = self.menuBar()

        #----------File------------------------#

        self.current_file = "./Default.csv"

        self.file_menu = self.menu_bar.addMenu("File")

        self.open_file_action = QAction("Open", self)
        self.open_file_action.triggered.connect(self.openFile)
        self.file_menu.addAction(self.open_file_action)

        #------------GraphsConfig------------#

        self.graph_prop_class = GraphClass()

        self.graph_prop = self.menu_bar.addMenu("Graph Properties")

        self.graph_prop_action = QAction("Configure graph")
        self.graph_prop_action.triggered.connect(self.open_graph_properties)
        self.graph_prop.addAction(self.graph_prop_action)

        #----------------WIDGETS----------------#
        
        self.canvas = MplCanvas(self)

        self.readingLabel = QLabel("Select or drag and drop a csv file to start")

        layout = QGridLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.addWidget(self.readingLabel,0,0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.canvas, 1,0,1,2)
        
        layout.setRowStretch(0,0)
        layout.setRowStretch(1,1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, a0):
        if a0.mimeData().hasUrls():
            for url in a0.mimeData().urls():
                if url.toLocalFile().endswith(".csv"):
                    a0.acceptProposedAction()
                    return
        a0.ignore()
    
    def dropEvent(self, a0):
        for url in a0.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".csv"):
                self.current_file = file_path
                self.graphPlotter(file_path)
            else:
                QMessageBox.warning(self, "INVALID FILE", "PLEASE DROP A CSV FILE")
    
    def graphPlotter(self, file_path):

        self.canvas.ax.clear()

        self.readingLabel.setText("Now reading: " + file_path)
        dataFrame = pd.read_csv(file_path)

        X = dataFrame.iloc[:, 0].tolist()
        X.pop(0)

        X = pd.to_numeric(X, errors='coerce')

        for cols in range(len(dataFrame.columns)-1):
            if(not self.graph_prop_class.visibility[cols]):
                continue
            Y = dataFrame.iloc[:, cols+1].tolist()
            Y.pop(0)
            for i in range(len(Y)):
                Y[i] = self.graph_prop_class.scaleFactor * float(Y[i]) + self.graph_prop_class.displacementFactor
                #bode
                #Y[i] = 20*np.log10(Y[i])
            self.canvas.ax.plot(X, Y, label=dataFrame.columns.tolist()[cols+1])
            if self.graph_prop_class.findMax:
                maxValueIndex = np.argmax(Y)
                self.canvas.ax.plot(X[maxValueIndex], Y[maxValueIndex], 'x')
                self.canvas.ax.annotate("Max in (" + str(X[maxValueIndex]) + ", " + str(Y[maxValueIndex]) + ")", (X[maxValueIndex], Y[maxValueIndex]), textcoords="offset points", xytext=(0,10), ha='center')
            if self.graph_prop_class.findMin:
                minValueIndex = np.argmin(Y)
                self.canvas.ax.plot(X[minValueIndex], Y[minValueIndex],'x')
                self.canvas.ax.annotate("Min in (" + str(X[minValueIndex]) + ", " + str(Y[minValueIndex]) + ")", (X[minValueIndex], Y[minValueIndex]), textcoords="offset points", xytext=(0,10), ha='center')

        self.canvas.ax.set_xscale(self.graph_prop_class.x_scale)
        self.canvas.ax.set_yscale(self.graph_prop_class.y_scale)
        self.canvas.ax.set_xlabel(self.graph_prop_class.x_label)
        self.canvas.ax.set_ylabel(self.graph_prop_class.y_label)
        self.canvas.ax.set_title(self.graph_prop_class.title)

        self.canvas.ax.grid(self.graph_prop_class.addGrid)

        mplcursors.cursor(self.canvas.ax, hover=True)
        self.canvas.ax.legend()
        self.canvas.draw()

    def openFile(self):
        file_path, _= QFileDialog.getOpenFileName(self, "Open a file", "", "CSV Files (*.csv);;All Files (*)")
        if file_path.endswith(".csv"):
            self.current_file = file_path
            self.graphPlotter(file_path)
        else:
            QMessageBox.warning(self, "INVALID FILE", "PLEASE DROP A CSV FILE")
    
    def open_graph_properties(self):
        self.graph_properties = GraphProperties(self.graph_prop_class, self)
        self.graph_properties.updated.connect(lambda: self.graphPlotter(self.current_file))
        self.graph_properties.show()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())