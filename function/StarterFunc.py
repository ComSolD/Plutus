from interface.MainWindow import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSizeGrip, QDesktopWidget
from PyQt5.QtCore import Qt

from function import Clicked, Settings


class Starter(Clicked, Settings, QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def starter(self):
        self.change_home_page()
        self.clicked_button()
        self.settings()