import cv2
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Thread(QThread):
    change_pixel_map = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture("auto.mp4")
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, channel = rgbImage.shape
                bytesPerLine = channel * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1080, 1080, Qt.KeepAspectRatio)
                self.change_pixel_map.emit(p)


class WidgetGallery(QMainWindow):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.progressBar = QProgressBar()
       # self.bottomRightGroupBox = QGroupBox("Group 3")
        self.bottomRightTabWidget = QTabWidget()
        self.bottomLeftTabWidget = QTabWidget()
        self.topRightGroupBox = QGroupBox("Group 2")
        self.topLeftGroupBox = QGroupBox("Group 1")
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightTabWidget()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightTabWidget.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightTabWidget, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        gridWidget = QWidget()
        gridWidget.setLayout(mainLayout)
        self.setCentralWidget(gridWidget)
        self.setMinimumSize(3840, 2160)

        self.setWindowTitle("Rover UI")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if self.useStylePaletteCheckBox.isChecked():
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTopLeftGroupBox(self):
        # radioButton1 = QRadioButton("Radio button 1")
        # radioButton2 = QRadioButton("Radio button 2")
        # radioButton3 = QRadioButton("Radio button 3")
        # radioButton1.setChecked(True)

        # checkBox = QCheckBox("Tri-state check box")
        # checkBox.setTristate(True)
        # checkBox.setCheckState(Qt.PartiallyChecked)
        self.videoStream()

        layout = QVBoxLayout()
        layout.addWidget(self.videoLabel)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def setImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def videoStream(self):
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(1280, 960)
        th = Thread(self)
        th.change_pixel_map.connect(self.setImage)
        th.start()

    def createTopRightGroupBox(self):
        startSwitch = QPushButton("Rover Bring Up")
        startSwitch.setDefault(True)
        startSwitch.setMaximumSize(300, 100)
        offSwitch = QPushButton("Rover Shutdown")
        offSwitch.setDefault(True)
        offSwitch.setMaximumSize(300, 100)

        layout = QVBoxLayout()
        layout.addWidget(startSwitch)
        layout.addWidget(offSwitch)
        # layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        '''self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

        h_headers = ["data", "time"]
        v_headers = ["GPS", "velocity", "Voltage", "mode", "heading"]

        tab1 = QWidget()
        tableWidget = QTableWidget(5, 2)
        tableWidget.setHorizontalHeaderLabels(h_headers)
        tableWidget.setVerticalHeaderLabels(v_headers)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")'''

    def createBottomRightTabWidget(self):
        self.bottomRightTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                               QSizePolicy.Ignored)

        h_headers = ["data", "time"]
        v_headers = ["GPS", "velocity", "Voltage", "mode", "heading"]

        tab1 = QWidget()
        tableWidget = QTableWidget(5, 2)
        tableWidget.setHorizontalHeaderLabels(h_headers)
        tableWidget.setVerticalHeaderLabels(v_headers)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n"
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n"
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomRightTabWidget.addTab(tab1, "&Table")
        self.bottomRightTabWidget.addTab(tab2, "Text &Edit")

        # self.bottomRightGroupBox.setCheckable(True)
        # self.bottomRightGroupBox.setChecked(True)

        # lineEdit = QLineEdit('s3cRe7')
        # lineEdit.setEchoMode(QLineEdit.Password)

        # spinBox = QSpinBox(self.bottomRightGroupBox)
        # spinBox.setValue(50)

        # dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        # dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        # slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        # slider.setValue(40)

        # scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        # scrollBar.setValue(60)

        # dial = QDial(self.bottomRightGroupBox)
        # dial.setValue(30)
        # dial.setNotchesVisible(True)

        # layout = QGridLayout()
        # layout.addWidget(lineEdit, 0, 0, 1, 2)
        # layout.addWidget(spinBox, 1, 0, 1, 2)
        # layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        # layout.addWidget(slider, 3, 0)
        # layout.addWidget(scrollBar, 4, 0)
        # layout.addWidget(dial, 3, 1, 2, 1)
        # layout.setRowStretch(5, 1)
        # self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
