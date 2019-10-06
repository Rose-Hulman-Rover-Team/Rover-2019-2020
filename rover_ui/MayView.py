from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtWebEngineWidgets 
from PyQt5.QtPrintSupport import *
import sys
import sqlite3
import time
import os

class InsertDialog(QDialog):
    def __init__(self, conn, table):
        super(InsertDialog, self).__init__()

        self.setWindowTitle("加入新产品")
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)

        self.table = table
        self.conn = conn

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.scroll.setWidget(scroll_widget)
        layout = QVBoxLayout(scroll_widget)

        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("名称")
        layout.addWidget(self.nameInput)

        self.typeInput = QLineEdit()
        self.typeInput.setPlaceholderText("型号")
        layout.addWidget(self.typeInput)

        self.colorInput = QLineEdit()
        self.colorInput.setPlaceholderText("颜色")
        layout.addWidget(self.colorInput)

        self.weightInput = QLineEdit()
        self.weightInput.setPlaceholderText("重量")
        layout.addWidget(self.weightInput)
        
        self.sizeInput = QLineEdit()
        self.sizeInput.setPlaceholderText("尺寸")
        layout.addWidget(self.sizeInput)

        self.packingInput = QLineEdit()
        self.packingInput.setPlaceholderText("包装形式")
        layout.addWidget(self.packingInput)

        self.packingWeight = QLineEdit()
        self.packingWeight.setPlaceholderText("包装重量")
        layout.addWidget(self.packingWeight)

        self.packingSize = QLineEdit()
        self.packingSize.setPlaceholderText("包装尺寸")
        layout.addWidget(self.packingSize)

        self.featureInput = QLineEdit()
        self.featureInput.setPlaceholderText("产品特点")
        self.featureInput.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        layout.addWidget(self.featureInput)
        
        self.descriptionInput = QLineEdit()
        self.descriptionInput.setPlaceholderText("产品描述")
        self.descriptionInput.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        layout.addWidget(self.descriptionInput)

        self.keywordInput = QLineEdit()
        self.keywordInput.setPlaceholderText("产品关键词")
        self.keywordInput.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        layout.addWidget(self.keywordInput)

        self.photo1Input = QLineEdit()
        self.photo1Input.setPlaceholderText("图片1")
        layout.addWidget(self.photo1Input)

        self.photo2Input = QLineEdit()
        self.photo2Input.setPlaceholderText("图片2")
        layout.addWidget(self.photo2Input)

        self.photo3Input = QLineEdit()
        self.photo3Input.setPlaceholderText("图片3")
        layout.addWidget(self.photo3Input)

        self.photo4Input = QLineEdit()
        self.photo4Input.setPlaceholderText("图片4")
        layout.addWidget(self.photo4Input)

        self.photo5Input = QLineEdit()
        self.photo5Input.setPlaceholderText("图片5")
        layout.addWidget(self.photo5Input)

        self.photo6Input = QLineEdit()
        self.photo6Input.setPlaceholderText("图片6")
        layout.addWidget(self.photo6Input)

        self.photo7Input = QLineEdit()
        self.photo7Input.setPlaceholderText("图片7")
        layout.addWidget(self.photo7Input)

        self.photo8Input = QLineEdit()
        self.photo8Input.setPlaceholderText("图片8")
        layout.addWidget(self.photo8Input)

        self.photo9Input = QLineEdit()
        self.photo9Input.setPlaceholderText("图片9")
        layout.addWidget(self.photo9Input)

        self.photo10Input = QLineEdit()
        self.photo10Input.setPlaceholderText("图片10")
        layout.addWidget(self.photo10Input)

        self.QBtn = QPushButton()
        self.QBtn.setText("确认")
        self.QBtn.clicked.connect(self.addstudent)
        layout.addWidget(self.QBtn)

        lay_all = QVBoxLayout()
        lay_all.addWidget(self.scroll)
        self.setLayout(lay_all)

    def addstudent(self):
        try:
            with self.conn.cursor() as cursor:
                command = "INSERT INTO {} values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);".format(self.table)
                name = self.nameInput.text()
                model = self.typeInput.text()
                color = self.colorInput.text()
                size = self.sizeInput.text()
                weight = self.weightInput.text()
                ptype = self.packingInput.text()
                psize = self.packingSize.text()
                pweight = self.packingWeight.text()
                feature = self.featureInput.text()
                desc = self.descriptionInput.text()
                keyword = self.keywordInput.text()
                p1 = self.photo1Input.text()
                p2 = self.photo2Input.text()
                p3 = self.photo3Input.text()
                p4 = self.photo4Input.text()
                p5 = self.photo5Input.text()
                p6 = self.photo6Input.text()
                p7 = self.photo7Input.text()
                p8 = self.photo8Input.text()
                p9 = self.photo9Input.text()
                p10 = self.photo10Input.text()
                cursor.execute(command, (name,model,color,size,weight,ptype,psize,pweight,feature,keyword,desc,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10))
                self.conn.commit()
        
            QMessageBox.information(QMessageBox(),'Successful','producted is added successfully to the database.')
            self.close()
        except Exception as e:
            QMessageBox.information(QMessageBox(),'Error','producted cannot be added to the database.')

class SearchDialog(QDialog):
    def __init__(self, conn, table):
        super(SearchDialog, self).__init__()
        self.conn = conn
        self.table = table
       
        self.QBtn = QPushButton()
        self.QBtn.setText("确认")

        self.setWindowTitle("检索产品")
        self.setFixedWidth(512)
        self.setFixedHeight(512)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.searchinput.setPlaceholderText("产品名称")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):
        name = self.searchinput.text()
        try:
            with self.conn.cursor() as cursor:
                command = "SELECT * FROM {} WHERE name=%s".format(self.table)
                cursor.execute(command, (name))
                self.conn.commit()
                record = cursor.fetchone()
                table = TableDialog(record)
                table.exec_()
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            print(getattr(e, 'message', str(e)))
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Find product from the database.')

class TableDialog(QDialog):
    def __init__(self, record):
        super(TableDialog, self).__init__()
        self.record = record

        self.setWindowTitle("检索产品")
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)

        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(21)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Label", "Data"))
        headers = ["名称", "型号", "颜色", 
                    "尺寸", "重量","包装形式","包装尺寸","包装重量",
                    "产品特点","产品描述","产品关键词","图片1",
                    "图片2","图片3","图片4","图片5","图片6",
                    "图片7","图片8","图片9","图片10"]
        i = 0
        for header in headers:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(header))
            i+=1
        self.load_data()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def load_data(self):
        i = 0
        for key in self.record:
            if isinstance(self.record, dict):
                self.tableWidget.setItem(i, 1, QTableWidgetItem(self.record[key]))
            else:
                self.tableWidget.setItem(i, 1, QTableWidgetItem(key))
            i += 1

class ModifyDialog(QDialog):
    def __init__(self, conn, table):
        super(ModifyDialog, self).__init__()
        self.conn = conn
        self.table = table
        self.QBtn = QPushButton()
        self.QBtn.setText("确认") 

        self.setWindowTitle("更改数据")
        self.setFixedWidth(512)
        self.setFixedHeight(512)
        self.QBtn.clicked.connect(self.modify)

        layout = QVBoxLayout()

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("产品名称")
        self.labelinput = QLineEdit()
        self.labelinput.setPlaceholderText("数据名称")
        self.valinput = QLineEdit()
        self.valinput.setPlaceholderText("新数据值")

        layout.addWidget(self.nameinput)
        layout.addWidget(self.labelinput)
        layout.addWidget(self.valinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

        self.product_query = {}
        self.product_query['名称'] = "UPDATE {} SET name=%s WHERE name=%s".format(self.table) 
        self.product_query['型号'] = "UPDATE {} SET type=%s WHERE name=%s".format(self.table)
        self.product_query['颜色'] = "UPDATE {} SET color=%s WHERE name=%s".format(self.table)
        self.product_query['尺寸'] = "UPDATE {} SET size=%s WHERE name=%s".format(self.table)
        self.product_query['重量'] = "UPDATE {} SET weight=%s WHERE name=%s".format(self.table)
        self.product_query['包装形式'] = "UPDATE {} SET ptype=%s WHERE name=%s".format(self.table)
        self.product_query['包装尺寸'] = "UPDATE {} SET psize=%s WHERE name=%s".format(self.table)
        self.product_query['包装重量'] = "UPDATE {} SET pweight=%s WHERE name=%s".format(self.table)
        self.product_query['产品特点'] = "UPDATE {} SET feature=%s WHERE name=%s".format(self.table)
        self.product_query['产品描述'] = "UPDATE {} SET desc=%s WHERE name=%s".format(self.table)
        self.product_query['产品关键词'] = "UPDATE {} SET keyword=%s WHERE name=%s".format(self.table)

    def modify(self):
        try:
            with self.conn.cursor() as cursor:
                name = self.nameinput.text()
                lable = self.labelinput.text()
                val = self.valinput.text()
                command = self.product_query[lable]
                cursor.execute(command, (val, name))
                self.conn.commit()
            QMessageBox.information(QMessageBox(),'Successful','producted is successfully modified.')
            self.close()
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            print(getattr(e, 'message', str(e)))
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not modify product in the database.')
            
class DeleteDialog(QDialog):
    def __init__(self, conn, table):
        super(DeleteDialog, self).__init__()
        self.conn = conn
        self.table = table
        
        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Student")
        self.setFixedWidth(512)
        self.setFixedHeight(512)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.deleteinput.setPlaceholderText("产品名称")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):
        name = self.deleteinput.text()
        try:
            with self.conn.cursor() as cursor:
                command = "DELETE FROM {} where name =%s".format(self.table)
                cursor.execute(command, (name))
                self.conn.commit()
            QMessageBox.information(QMessageBox(),'Successful','Deleted From Table')    
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not delete product from the database.')

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(250)

        QBtn = QDialogButtonBox.Ok  
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        
        self.setWindowTitle("About")
        title = QLabel("Student Record Maintainer In PyQt5")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/dexter.jpg')
        pixmap = pixmap.scaledToWidth(275)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(150)

        layout.addWidget(title)

        layout.addWidget(QLabel("v2.0"))
        layout.addWidget(QLabel("Copyright Okay Dexter 2019"))
        layout.addWidget(labelpic)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QIcon('icon/fish.jpg')) 
        self.setWindowTitle("ROSE ROVER UI")

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
        self.combobox.activated[str].connect(self.setTable)

        toolbar.addWidget(self.combobox)

        '''btn_ac_connect = QAction(QIcon("icon/conn.png"), "Connect to Database", self)
        btn_ac_connect.triggered.connect(self.connect)
        btn_ac_connect.setStatusTip("连接数据库")
        toolbar.addAction(btn_ac_connect)

        btn_ac_shutdown = QAction(QIcon("icon/shut.png"), "Connect to Database", self)
        btn_ac_shutdown.triggered.connect(self.close)
        btn_ac_shutdown.setStatusTip("关闭数据库")
        toolbar.addAction(btn_ac_shutdown)

        btn_ac_adduser = QAction(QIcon("icon/add.png"), "添加产品", self)   #add student icon
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("添加新产品")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/r3.png"),"刷新",self)   #refresh icon
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("刷新表格")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_modify = QAction(QIcon("icon/modify.png"), "更新数据", self)
        btn_ac_modify.triggered.connect(self.modify)
        btn_ac_modify.setStatusTip("更新产品信息")
        toolbar.addAction(btn_ac_modify)

        btn_ac_search = QAction(QIcon("icon/s1.png"), "检索产品", self)  #search icon
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("检索产品信息")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/d1.png"), "删除产品", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("删除产品")
        toolbar.addAction(btn_ac_delete)

        add_action = QAction(QIcon("icon/add.png"),"添加产品", self)
        add_action.triggered.connect(self.insert)
        file_menu.addAction(add_action)

        searchuser_action = QAction(QIcon("icon/s1.png"), "检索产品", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        modify_acction = QAction(QIcon("icon/modify.png"), "更新数据")
        modify_acction.triggered.connect(self.modify)
        file_menu.addAction(modify_acction)

        delete_action = QAction(QIcon("icon/d1.png"), "删除产品", self)
        delete_action.triggered.connect(self.delete)
        file_menu.addAction(delete_action)

        self.login()'''

    def set_table(self):
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        headers = ["名称", "型号", "颜色", "尺寸", "重量",
                    "包装形式","包装尺寸","包装重量",
                    "产品特点","产品描述","产品关键词"]
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.repaint()
        self.loaddata()

    def loaddata(self):
        self.connect()
        if self.table == "":
            self.table = "Ebay"
        query = "SELECT * FROM {}".format(self.table)
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()
            result = cursor.fetchall()
            self.tableWidget.setRowCount(0)
            i = 0
            for row in result:
                self.tableWidget.insertRow(i)
                j = 0
                for key in row:
                    if isinstance(row, dict):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(row[key]))
                    else:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(key))
                    j += 1
                i += 1
        self.conn.close()
    
    def setTable(self, text):
        self.table = text

    def connect(self):
        if not self.config:
            self.config['host'] = 'localhost'
            self.config['port'] = 3306
            self.config['user'] = self.username.text()
            self.config['password'] = self.password.text()
            self.config['db'] = self.db.text()
            self.config['charset'] = 'utf8mb4'
            self.config['cursorclass'] = sql.cursors.DictCursor
        try:
            self.conn = sql.connect(**self.config)
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not connect to the database.')

    def close_connection(self):
        self.conn.close()
        self.close()

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

    def login(self):
        groupBox = QGroupBox("登录数据库")
        
        QBtn = QPushButton("确认")
        QBtn.clicked.connect(self.set_table)

        QBtn2 = QPushButton("注册")
        QBtn2.clicked.connect(self.register)

        layout = QVBoxLayout()

        self.db = QLineEdit()
        self.db.setPlaceholderText("数据库名称")
        layout.addWidget(self.db)

        self.host = QLineEdit()
        self.host.setPlaceholderText("地址")
        layout.addWidget(self.host)

        self.port = QLineEdit()
        self.port.setPlaceholderText("端口")
        layout.addWidget(self.port)

        self.username = QLineEdit()
        self.username.setPlaceholderText("账号")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("密码")
        layout.addWidget(self.password)
        layout.addWidget(QBtn)
        layout.addWidget(QBtn2)
        layout.addStretch(1)
        
        groupBox.setLayout(layout)
        self.setCentralWidget(groupBox)
    
    def register(self):
        #self.connect = sql.connect(db.)
        username = self.username.text()
        password = self.password.text()

        try:
            with self.conn.cursor() as cursor:
                command1 = "CREATE USER '{}'@'localhost' IDENTIFIED BY '{}';".format(username, password)
                command2 = "GRANT ALL PRIVILEGES ON *.* TO '%s'@'localhost';"%(username)
                QMessageBox.warning(QMessageBox(), 'Successful', 'new user is added to the database')
        except Exception as e:
            print(getattr(e, 'message', repr(e)))
            print(getattr(e, 'message', str(e)))
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add the user to the database')


    def insert(self):
        self.connect()
        dlg = InsertDialog(self.conn, self.table)
        dlg.exec_()
        self.conn.close()

    def modify(self):
        self.connect()
        dlg = ModifyDialog(self.conn, self.table)
        dlg.exec_()
        self.conn.close()

    def delete(self):
        self.connect()
        dlg = DeleteDialog(self.conn, self.table)
        dlg.exec_()
        self.conn.close()

    def search(self):
        self.connect()
        dlg = SearchDialog(self.conn, self.table)
        dlg.exec_()
        self.conn.close()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

app = QApplication(sys.argv)
if(QDialog.Accepted == True):
    window = MainWindow()
    window.show()
sys.exit(app.exec_())