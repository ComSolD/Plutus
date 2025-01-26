from interface.MainWindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAbstractSpinBox
from PyQt5.QtCore import Qt, QDate

import datetime

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    
    def callParserInterface(self):
        self.ui.FirstDate = QtWidgets.QDateEdit(self.ui.MainWidget)
        self.ui.FirstDate.setGeometry(QtCore.QRect(50, 60, 719, 198))
        self.ui.FirstDate.setStyleSheet("QDateEdit{\n"
"color: #CCCCCC;\n"
"font-size: 182px;\n"
"background-color: #501F3A;\n"
"border-radius: 7px;\n"
"selection-background-color: #CB2D6F;\n"
"selection-color: white;\n"
"}")
        self.ui.FirstDate.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.FirstDate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ui.FirstDate.setObjectName("FirstDate")
        self.ui.SecondDate = QtWidgets.QDateEdit(self.ui.MainWidget)
        self.ui.SecondDate.setGeometry(QtCore.QRect(-170, 320, 719, 222))
        self.ui.SecondDate.setStyleSheet("QDateEdit{\n"
"color: #CCCCCC;\n"
"font-size: 182px;\n"
"background-color: #501F3A;\n"
"border-radius: 7px;\n"
"selection-background-color: #CB2D6F;\n"
"selection-color: white;\n"
"}")
        self.ui.SecondDate.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.SecondDate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ui.SecondDate.setObjectName("SecondDate")
        self.ui.GetDataWidget = QtWidgets.QWidget(self.ui.MainWidget)
        self.ui.GetDataWidget.setGeometry(QtCore.QRect(-50, 600, 719, 50))
        self.ui.GetDataWidget.setMinimumSize(QtCore.QSize(0, 50))
        self.ui.GetDataWidget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ui.GetDataWidget.setObjectName("GetDataWidget")
        self.ui.horizontalLayout = QtWidgets.QHBoxLayout(self.ui.GetDataWidget)
        self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ui.horizontalLayout.setObjectName("horizontalLayout")


        self.ui.ParserLabel = QtWidgets.QLabel(self.ui.MenuWidget)
        self.ui.ParserLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.ParserLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ui.ParserLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ui.ParserLabel.setStyleSheet("QLabel{\n"
"color: white;\n"
"font-size: 32px;\n"
"font-family: Century Schoolbook;\n"
"}")
        self.ui.ParserLabel.setText("")
        self.ui.ParserLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ParserLabel.setObjectName("ParserLabel")
        self.ui.horizontalLayout.addWidget(self.ui.ParserLabel)

        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ui.horizontalLayout.addItem(spacerItem7)


        self.ui.DailyDataButton = QtWidgets.QPushButton(self.ui.GetDataWidget)
        self.ui.DailyDataButton.setMinimumSize(QtCore.QSize(200, 35))
        self.ui.DailyDataButton.setMaximumSize(QtCore.QSize(200, 35))
        self.ui.DailyDataButton.setStyleSheet("QPushButton{\n"
"background-color: #501F3A;\n"
"font-size: 28px;\n"
"color: #CCCCCC;\n"
"border-radius: 7px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #CB2D6F;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: #CB2D6F;\n"
"}")
        self.ui.DailyDataButton.setObjectName("DailyDataButton")
        self.ui.horizontalLayout.addWidget(self.ui.DailyDataButton)
        

        self.ui.GetDataButton = QtWidgets.QPushButton(self.ui.GetDataWidget)
        self.ui.GetDataButton.setMinimumSize(QtCore.QSize(200, 35))
        self.ui.GetDataButton.setMaximumSize(QtCore.QSize(200, 35))
        self.ui.GetDataButton.setStyleSheet("QPushButton{\n"
"background-color: #501F3A;\n"
"font-size: 28px;\n"
"color: #CCCCCC;\n"
"border-radius: 7px;\n"
"}\n"
"QPushButton:hover{\n"
"background-color: #CB2D6F;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: #CB2D6F;\n"
"}")
        self.ui.GetDataButton.setObjectName("GetDataButton")
        self.ui.horizontalLayout.addWidget(self.ui.GetDataButton)

        _translate = QtCore.QCoreApplication.translate

        self.ui.GetDataButton.setText(_translate("MainWindow", "Сбор данных"))
        self.ui.DailyDataButton.setText(_translate("MainWindow", "Быстрый сбор"))
        
        self.ui.FirstDate.setMinimumDate(QDate(2020, 1, 1))
        self.ui.SecondDate.setMinimumDate(QDate(2020, 1, 1))

        self.ui.FirstDate.setDate(datetime.date.today())
        self.ui.SecondDate.setDate(datetime.date.today())

        self.MainWidget.addWidget(self.ui.FirstDate)
        self.MainWidget.addWidget(self.ui.SecondDate)
        self.MainWidget.addWidget(self.ui.GetDataWidget)
