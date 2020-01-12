<<<<<<< HEAD:rover_ui/MainView.py
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets 
from PyQt5.QtPrintSupport import *
import qdarkstyle
import sys
import sqlite3
import time
import os
import cv2

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.setWindowIcon()
        self.setWindowTitle("ROSE ROVER UI")

        self.dataKeys = ["Can Data", "GPS Coordinates", "X_Speed", "Y_Speed", "PDP","connection_status"]

        self.setMinimumSize(800, 600)
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&About")

        self.tableWidget = QTableWidget()

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.combobox = QComboBox()
        self.combobox.setObjectName(("Stage"))
        self.combobox.addItem("Autonomus")
        self.combobox.addItem("Science")
        self.combobox.addItem("Equipment")
        #self.combobox.activated[str].connect(self.set_table())

        toolbar.addWidget(self.combobox)
        
        self.set_table()
        self.videoStream()
        self.createHorizontalLayout()

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.tableWidget, 0)
        layout.addWidget(self.videoLabel, 0)
        self.horizontalGroupBox.setLayout(layout)  
        self.setCentralWidget(self.horizontalGroupBox)

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def set_table(self): 
        self.tableWidget.move(0,0)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(self.dataKeys))

        for row in range(len(self.dataKeys)):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.dataKeys[row]))

        headers = ["name", "value", "time"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.repaint()

    #@pyqtSlot(QImage)
    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def videoStream(self):
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(1280, 960)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if(QDialog.Accepted == True):
        window = MainWindow()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window.show()
=======
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets 
from PyQt5.QtPrintSupport import *
import qdarkstyle
import sys
import sqlite3
import time
import os
import cv2

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.setWindowIcon()
        self.setWindowTitle("ROSE ROVER UI")

        self.dataKeys = ["Can Data", "GPS Coordinates", "X_Speed", "Y_Speed", "PDP","connection_status"]

        self.setMinimumSize(800, 600)
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&About")

        self.tableWidget = QTableWidget()

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        self.combobox = QComboBox()
        self.combobox.setObjectName(("Stage"))
        self.combobox.addItem("Autonomus")
        self.combobox.addItem("Science")
        self.combobox.addItem("Equipment")
        #self.combobox.activated[str].connect(self.set_table())

        toolbar.addWidget(self.combobox)
        
        self.set_table()
        self.videoStream()
        self.createHorizontalLayout()

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.tableWidget, 0)
        layout.addWidget(self.videoLabel, 0)
        self.horizontalGroupBox.setLayout(layout)  
        self.setCentralWidget(self.horizontalGroupBox)

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def set_table(self): 
        self.tableWidget.move(0,0)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(self.dataKeys))

        for row in range(len(self.dataKeys)):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.dataKeys[row]))

        headers = ["name", "value", "time"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.repaint()

    #@pyqtSlot(QImage)
    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def videoStream(self):
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(1280, 960)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if(QDialog.Accepted == True):
        window = MainWindow()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window.show()
>>>>>>> f21c786e9956ecc636c2c538a7456a9174a90a6a:rover_ui/MainView.py
    sys.exit(app.exec_())