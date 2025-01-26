from interface.MainWindow import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAbstractSpinBox
from PyQt5.QtCore import Qt


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    
    def callHomeInterface(self):
        self.ui.HomeTextEdit = QtWidgets.QTextEdit(self.ui.MainWidget)
        self.ui.HomeTextEdit.setEnabled(True)
        self.ui.HomeTextEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.ui.HomeTextEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ui.HomeTextEdit.setStyleSheet("QTextEdit{\n"
"color: white;\n"
"border: none;\n"
"selection-background-color: #501F3A;\n"
"selection-color: #CCCCCC;\n"
"}\n"
"")
        self.ui.HomeTextEdit.setReadOnly(True)
        self.ui.HomeTextEdit.setObjectName("HomeTextEdit")

        h_scrollbar = self.ui.HomeTextEdit.horizontalScrollBar()
        v_scrollbar = self.ui.HomeTextEdit.verticalScrollBar()

        h_scrollbar.setContextMenuPolicy(Qt.NoContextMenu)
        v_scrollbar.setContextMenuPolicy(Qt.NoContextMenu)

        self.ui.HomeTextEdit.setContextMenuPolicy(Qt.NoContextMenu)


        _translate = QtCore.QCoreApplication.translate

        self.ui.HomeTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Cambria\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">Правила для игры на ставках:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">1. Ставить только 5% от своего банка округленного в меньшую сторону. Пример: на балансе 2675, следовательно сумма ставки равна 100.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">2. Не ставить на коэффициент ниже 1.7, так как риск будет являться не оправданным. Пример: Сделал 10 ставок с коэффициентом 1.5, чтобы выйти в плюс, потребуется винрейт в 70%, а при 1.7 - 60%.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">3. Брать перерыв после минусов, так как после этого хочется отыграться, а следоватьно совершить не обдуманные действия. Пример: каждый день выходил в плюс по балансу прошлого дня, но в этот раз вышел в минус, после чего ставишь сумму, которая перекрывает потерю.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">4. Не ставить на направление, в которых не разбираешься. Пример: большой теннис или CS2.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Century Schoolbook\'; font-size:18pt;\">5. Не смотреть трансляции. Ситуации в игре поталкивают на необдуманные действия. Либо контролировать свои эмоции, что является не обычайно трудно. Пример: происходит противоложное событие, не перекрыть проигрышь новой ставкой.</span></p></body></html>"))


        self.MainWidget.addWidget(self.ui.HomeTextEdit)

        