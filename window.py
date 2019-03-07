import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.Qt import *
import corrections as cor1

# cor = cor.corrections()

class window(QWidget):
    def __init__(self):
        super(window, self).__init__()
        self.initUI()

    def initUI(self):

        # Labels
        cor_type = QLabel('Correction Type')
        cor = QLabel('List of Correction')
        input = QLabel('Input image path')
        output = QLabel('Output image path')
        self.sa_label = QLabel('Enter sun angle in xx.xx format')
        self.dosv_label = QLabel('Enter minimum values of each band as list xx,xx,xx,..')


        # Buttons
        inputImage = QPushButton('Select Input Image')
        outputImage = QPushButton('Select Output Image')
        self.runButton = QPushButton('Run')
        self.runButton.toggle()
        cancelButton = QPushButton('Exit', self)

        # Dropbox
        self.comboBox1 = QComboBox()
        self.comboBox1.addItems(['Select', 'Atmosperic Corrections', 'Imperfection of sensor', 'Image Enhancement'])
        self.comboBox2 = QComboBox()
        self.comboBox2.addItems(['Select'])
        self.comboBox1.currentTextChanged.connect(self.updateComboBox2)

        # Actions
        cancelButton.clicked.connect(self.buttonClicked)
        self.runButton.clicked.connect(self.runButtonClicked)

        # File Select
        inputImage.clicked.connect(self.getfile)
        outputImage.clicked.connect(self.savefile)

        # LineEdit
        self.inputName = QLineEdit('Input path')
        self.inputName.setReadOnly(True)
        self.outputName = QLineEdit('Output path')
        self.outputName.setReadOnly(True)
        self.paramValue = QLineEdit()

        # Grid
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(cor_type, 0, 0)
        self.grid.addWidget(self.comboBox1, 2, 0)
        self.grid.addWidget(cor, 3, 0)
        self.grid.addWidget(self.comboBox2, 4, 0)
        self.grid.addWidget(input, 5, 0)
        self.grid.addWidget(self.inputName, 6, 0)
        self.grid.addWidget(inputImage, 6, 1)
        self.grid.addWidget(output, 8, 0)
        self.grid.addWidget(self.outputName, 9, 0)
        self.grid.addWidget(outputImage, 9, 1)
        self.grid.addWidget(self.runButton, 10, 3)
        self.grid.addWidget(cancelButton, 10, 4)
        self.setLayout(self.grid)

        # Main Window
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle("Radiometric Corrections")
        self.setWindowIcon(QIcon('./data/pixels.jpg'))
        self.show()

    iname = None
    oname = None
    sa = None
    dosv = None

    def getfile(self):
        fgname = QFileDialog.getOpenFileName(self, 'Open file', '~/', "Tif files (*.tif)")
        global iname
        iname = fgname
        self.inputName.setText(iname[0])
        if self.comboBox2.currentText() == 'Sun Angle Corrections':
            self.grid.addWidget(self.sa_label, 7, 0)
            self.grid.addWidget(self.paramValue, 7, 1)
            self.paramValue.setValidator(QDoubleValidator(0.99, 99.99, 2))
        elif self.comboBox2.currentText() == 'Dark Object Subtraction':
            self.grid.addWidget(self.dosv_label, 7, 0)
            self.grid.addWidget(self.paramValue, 7, 1)

    def savefile(self):
        fsname = QFileDialog.getSaveFileName(self, 'Save file', '~/', "Tif files (*.tif)")
        global oname
        global sa
        global dosv
        oname = fsname
        self.outputName.setText(oname[0])
        if self.comboBox2.currentText() == 'Sun Angle Corrections':
            sa = float(self.paramValue.text())
        elif self.comboBox2.currentText() == 'Dark Object Subtraction':
            dosv = list(self.paramValue.text())

    def buttonClicked(self):
        # closing the application
        QtCore.QCoreApplication.instance().quit()

    def runButtonClicked(self):
        if self.comboBox2.currentText() == 'Dark Object Subtraction':
            cor1.dos(iname[0], oname[0])
            self.msgbox()
        elif self.comboBox2.currentText() == 'Sun Angle Corrections':
            cor1.sac(iname[0], oname[0], sa)
            self.msgbox()
        elif self.comboBox2.currentText() == 'Average Filter':
            cor1.avg_filter(iname[0], oname[0])
            self.msgbox()
        elif self.comboBox2.currentText() == 'Distance Weighted Average Filter':
            cor1.weighted_avg_filter(iname[0], oname[0])
            self.msgbox()
        elif self.comboBox2.currentText() == 'X-Gradient Filter':
            cor1.x_gradient_filter(iname[0], oname[0])
            self.msgbox()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Something Went Wrong, varify input details")
            msg.setWindowTitle("Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def updateComboBox2(self, newValue):

        if newValue == 'Select':
            self.comboBox2.clear()  # This will remove all previous items
            self.comboBox2.addItems(['Select'])

        elif newValue == 'Atmosperic Corrections':
            self.comboBox2.clear()
            self.comboBox2.addItems(['Select', 'Sun Angle Corrections', 'Dark Object Subtraction'])

        elif newValue == 'Imperfection of sensor':
            self.comboBox2.clear()
            self.comboBox2.addItems(['Select', 'Line drop Correction', 'Line strip correction', 'Pixel drop correction'])

        elif newValue == 'Image Enhancement':
            self.comboBox2.clear()
            self.comboBox2.addItems(['Select', 'Average Filter', 'Distance Weighted Average Filter', 'X-Gradient Filter', 'Y-Gradient Filter',
                                     'All-Directional Filter', 'Edge Enhancing Filter'])


    def msgbox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Successfully completed")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setWindowTitle("Message")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window()
    sys.exit(app.exec_())
