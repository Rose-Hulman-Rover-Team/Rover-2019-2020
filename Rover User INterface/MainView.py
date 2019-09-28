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

        layout = QGridLayout()
        layout.addWidget(self.tableWidget) 
        #self.layout.addWidget(self.label)
        self.setLayout(layout)

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
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(self.dataKeys))

        for row in range(len(self.dataKeys)):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.dataKeys[row]))

        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        headers = ["name", "value", "time"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.repaint()

    #@pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def videoStream(self):
        self.label = QLabel(self)
        self.label.move(720, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if(QDialog.Accepted == True):
        window = MainWindow()
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window.show()
    sys.exit(app.exec_())