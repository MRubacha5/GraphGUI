from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QFormLayout, QCheckBox, QDoubleSpinBox,
    QHBoxLayout)
from PyQt6.QtCore import pyqtSignal
from graph_class import GraphClass

class GraphProperties(QWidget):
    updated = pyqtSignal(GraphClass) 

    def __init__(self, graph_props: GraphClass, parent=None): #change current title
        super().__init__(parent)
        self.setWindowTitle("Edit graph properties")
        self.resize(600, 600)

        self.graph_props = graph_props

        layout = QFormLayout()

        self.title = QLineEdit(self.graph_props.title)
        self.xLabel = QLineEdit(self.graph_props.x_label)
        self.yLabel = QLineEdit(self.graph_props.y_label)

        self.checkboxLayout = QHBoxLayout()

        self.setCurve1 = QCheckBox("Curve 1")
        self.setCurve1.setChecked(self.graph_props.visibility[0])
        self.setCurve2 = QCheckBox("Curve 2")
        self.setCurve2.setChecked(self.graph_props.visibility[1])
        self.setCurve3 = QCheckBox("Curve 3")
        self.setCurve3.setChecked(self.graph_props.visibility[2])
        self.setCurve4 = QCheckBox("Curve 4")
        self.setCurve4.setChecked(self.graph_props.visibility[3])

        self.checkBoxContainer = QWidget()
        self.checkBoxContainer.setLayout(self.checkboxLayout)

        self.checkboxLayout.addWidget(self.setCurve1)
        self.checkboxLayout.addWidget(self.setCurve2)
        self.checkboxLayout.addWidget(self.setCurve3)
        self.checkboxLayout.addWidget(self.setCurve4)
        
        self.xScale = QComboBox()
        self.xScale.addItems(["linear", "log", "symlog", "logit"])
        self.xScale.setCurrentText(self.graph_props.x_scale)
        self.yScale = QComboBox()
        self.yScale.addItems(["linear", "log", "symlog", "logit"])
        self.yScale.setCurrentText(self.graph_props.y_scale)

        self.max = QCheckBox()
        self.max.setChecked(self.graph_props.findMax)
        self.min = QCheckBox()
        self.min.setChecked(self.graph_props.findMin)
        self.grid = QCheckBox()
        self.grid.setChecked(self.graph_props.addGrid)

        self.scaleFactor = QDoubleSpinBox()
        self.scaleFactor.setDecimals(2)
        self.scaleFactor.setSingleStep(0.01)
        self.scaleFactor.setValue(graph_props.scaleFactor)
        self.displacementFactor = QDoubleSpinBox()
        self.displacementFactor.setDecimals(2)
        self.displacementFactor.setSingleStep(0.01)
        self.displacementFactor.setValue(graph_props.displacementFactor)

        self.applyButton = QPushButton("Apply changes")
        self.applyButton.clicked.connect(self.apply_changes)

        layout.addRow("Title:", self.title)
        layout.addRow("X axis label:", self.xLabel)
        layout.addRow("Y axis label:", self.yLabel)
        layout.addRow("Choose visible curves:", self.checkBoxContainer)
        layout.addRow("X scale", self.xScale)
        layout.addRow("Y scale", self.yScale)
        layout.addRow("Find Max", self.max)
        layout.addRow("Find Min", self.min)
        layout.addRow("Add grid lines", self.grid)
        layout.addRow("Scale factor", self.scaleFactor)
        layout.addRow("Displacement factor", self.displacementFactor)
        layout.addRow(self.applyButton)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)


    def apply_changes(self):
        self.graph_props.title = self.title.text()
        self.graph_props.x_label = self.xLabel.text()
        self.graph_props.y_label = self.yLabel.text()
        self.graph_props.x_scale = self.xScale.currentText()
        self.graph_props.y_scale = self.yScale.currentText()
        self.graph_props.findMax = self.max.isChecked()
        self.graph_props.findMin = self.min.isChecked()
        self.graph_props.addGrid = self.grid.isChecked()
        self.graph_props.scaleFactor = self.scaleFactor.value()
        self.graph_props.displacementFactor = self.displacementFactor.value()
        self.graph_props.visibility[0] = self.setCurve1.isChecked()
        self.graph_props.visibility[1] = self.setCurve2.isChecked()
        self.graph_props.visibility[2] = self.setCurve3.isChecked()
        self.graph_props.visibility[3] = self.setCurve4.isChecked()

        self.updated.emit(self.graph_props)
        self.close()

