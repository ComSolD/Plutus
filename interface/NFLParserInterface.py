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

    
    def callNFLParserInterface(self):
        self.ui.NFLSettingsWidget = QtWidgets.QWidget(self.ui.MainWidget)
        self.ui.NFLSettingsWidget.setGeometry(QtCore.QRect(90, 210, 589, 200))
        self.ui.NFLSettingsWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.ui.NFLSettingsWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ui.NFLSettingsWidget.setStyleSheet("QComboBox::down-arrow {\n"
"    background: transparent;\n"
"}\n"
"QComboBox{\n"
"    background-color: #CB2D6F;\n"
"    font-size: 32px;\n"
"    color: #CCCCCC;\n"
"    border: 1px solid rgba(0,0,0,0.4);\n"
"    border-radius: 2px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    selection-color: #CCCCCC;\n"
"    color: #0F292F;\n"
"    selection-background-color: #CB2D6F;\n"
"    background-color: #CB2D6F;\n"
"    border: 1px solid rgba(0,0,0,0.4);\n"
"    border-radius: 0px;\n"
"    outline: 0px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"    width: 30px;\n"
"    height: 30px;\n"
"    background: transparent;\n"
"    padding: 0px 0px 0px 0px;\n"
"    margin-right: 5px;\n"
"    image: url(:/icon/icon/IconArrow.svg);\n"
"}\n"
"QComboBox::down-arrow:on {\n"
"    image: url(:/icon/icon/IconArrowLeft.svg);\n"
"}\n"
"QComboBox::drop-down{\n"
"    border: 0px;\n"
"}")
        self.ui.NFLSettingsWidget.setObjectName("NFLSettingsWidget")
        self.ui.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.ui.NFLSettingsWidget)
        self.ui.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.ui.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ui.YearDate = QtWidgets.QDateEdit(self.ui.NFLSettingsWidget)
        self.ui.YearDate.setMinimumSize(QtCore.QSize(640, 0))
        self.ui.YearDate.setStyleSheet("QDateEdit{\n"
"color: #CCCCCC;\n"
"font-size: 132px;\n"
"background-color: #501F3A;\n"
"border-radius: 7px;\n"
"selection-background-color: #CB2D6F;\n"
"selection-color: white;\n"
"}")
        self.ui.YearDate.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.YearDate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ui.YearDate.setObjectName("YearDate")
        self.ui.horizontalLayout_2.addWidget(self.ui.YearDate)
        self.ui.NFLOptionWidget = QtWidgets.QWidget(self.ui.NFLSettingsWidget)
        self.ui.NFLOptionWidget.setMinimumSize(QtCore.QSize(250, 0))
        self.ui.NFLOptionWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.ui.NFLOptionWidget.setObjectName("NFLOptionWidget")
        self.ui.verticalLayout_5 = QtWidgets.QVBoxLayout(self.ui.NFLOptionWidget)
        self.ui.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.ui.verticalLayout_5.setSpacing(40)
        self.ui.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ui.StageComboBox = QtWidgets.QComboBox(self.ui.NFLOptionWidget)
        self.ui.StageComboBox.setMinimumSize(QtCore.QSize(200, 50))
        self.ui.StageComboBox.setMaximumSize(QtCore.QSize(400, 50))
        self.ui.StageComboBox.setStyleSheet("")
        self.ui.StageComboBox.setMaxVisibleItems(5)
        self.ui.StageComboBox.setIconSize(QtCore.QSize(40, 40))
        self.ui.StageComboBox.setProperty("placeholderText", "")
        self.ui.StageComboBox.setObjectName("StageComboBox")
        self.ui.verticalLayout_5.addWidget(self.ui.StageComboBox)
        self.ui.TypeComboBox = QtWidgets.QComboBox(self.ui.NFLOptionWidget)
        self.ui.TypeComboBox.setMinimumSize(QtCore.QSize(200, 50))
        self.ui.TypeComboBox.setMaximumSize(QtCore.QSize(400, 50))
        self.ui.TypeComboBox.setStyleSheet("")
        self.ui.TypeComboBox.setMaxVisibleItems(100)
        self.ui.TypeComboBox.setIconSize(QtCore.QSize(40, 40))
        self.ui.TypeComboBox.setProperty("placeholderText", "")
        self.ui.TypeComboBox.setObjectName("TypeComboBox")
        self.ui.verticalLayout_5.addWidget(self.ui.TypeComboBox)
        self.ui.horizontalLayout_2.addWidget(self.ui.NFLOptionWidget)
        self.ui.GetDataWidget = QtWidgets.QWidget(self.ui.MainWidget)
        self.ui.GetDataWidget.setGeometry(QtCore.QRect(120, 510, 589, 50))
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

        self.ui.StageComboBox.setCurrentIndex(-1)
        self.ui.TypeComboBox.setCurrentIndex(-1)

        _translate = QtCore.QCoreApplication.translate

        self.ui.YearDate.setDisplayFormat(_translate("MainWindow", "yyyy"))
        self.ui.GetDataButton.setText(_translate("MainWindow", "Сбор данных"))

        self.ui.YearDate.setDate(datetime.date.today())

        self.ui.YearDate.setMinimumDate(QDate(2019, 1, 1))

        for i in range(1,19):
                self.ui.StageComboBox.addItem('Week ' + str(i))

        self.ui.StageComboBox.addItem('Wild Card')
        self.ui.StageComboBox.addItem('Divisional Round')
        self.ui.StageComboBox.addItem('Conf. Champ.')
        self.ui.StageComboBox.addItem('Super Bowl')

        self.ui.StageComboBox.addItem('Весь сезон')


        self.ui.StageComboBox.setEditable(True)
        self.ui.StageComboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.ui.StageComboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.ui.StageComboBox.completer().setMaxVisibleItems(5)

        stage_combo_box_line_edit = self.ui.StageComboBox.lineEdit()

        stage_combo_box_line_edit.setStyleSheet("selection-background-color: #501F3A;\n"
"    background-color: #CB2D6F;\n"
"    selection-color: white;\n"
"    font-size: 32px;\n"
"    outline: 0px;\n"
"    border: 1px solid rgba(0,0,0,0);\n"
"    border-radius: 2px;\n")

        self.ui.StageComboBox.completer().popup().setStyleSheet("QAbstractItemView {\n"
"    background-color: #CB2D6F;\n"
"    font-size: 32px;\n"
"    color: #0F292F;\n"
"    font-family: Cambria;\n"
"    border: 1px solid rgba(0,0,0,0.4);\n"
"    border-radius: 2px;\n"
"    selection-background-color: #CB2D6F;\n"
"    selection-color: #CCCCCC;\n"
"    outline: 0px;\n"
"}\n"
"QScrollBar:vertical{\n"
"    background-color: #CB2D6F;\n"
"}\n"
"\n"
"\n"
"\n"
"QScrollBar:vertical{\n"
"background-color: #501F3A;\n"
"border: none;\n"
"margin: 15px 0 15px 0;\n"
"width: 22px;\n"
"border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:vertical{\n"
"background-color: #CB2D6F;\n"
"min-height: 30px;\n"
"border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{\n"
"background-color: #AB275C;\n"
"}\n"
"QScrollBar::handle:vertical:pressed{\n"
"background-color: #AB275C;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical{\n"
"border: none;\n"
"background-color: #CB2D6F;\n"
"height: 15px;\n"
"border-top-left-radius: 7px;\n"
"border-top-right-radius: 7px;\n"
"subcontrol-position: top;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover{\n"
"background-color: #AB275C;\n"
"}\n"
"QScrollBar::sub-line:vertical:pressed{\n"
"background-color: #AB275C;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical{\n"
"border: none;\n"
"background-color: #CB2D6F;\n"
"height: 15px;\n"
"border-bottom-left-radius: 7px;\n"
"border-bottom-right-radius: 7px;\n"
"subcontrol-position: bottom;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical:hover{\n"
"background-color: #AB275C;\n"
"}\n"
"QScrollBar::add-line:vertical:pressed{\n"
"background-color: #AB275C;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{\n"
"background-color: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{\n"
"background-color: none;\n"
"}\n")

        self.ui.TypeComboBox.addItem('Собрать исходы')
        self.ui.TypeComboBox.addItem('Собрать предикты')


        self.MainWidget.addWidget(self.ui.NFLSettingsWidget)
        self.MainWidget.addWidget(self.ui.GetDataWidget)