from interface.MainWindow import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSizeGrip, QDesktopWidget
from PyQt5.QtCore import Qt


class Settings(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def settings(self):
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:
                    try:
                        self.move(self.pos() + e.globalPos() - self.clickPosition)
                    except AttributeError:
                        pass
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.ui.MenuWidget.mouseMoveEvent = moveWindow

        QSizeGrip(self.ui.size_grip)

        self.center()


    # Функции настройки окна

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
