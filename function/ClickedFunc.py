from interface.MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from function.OpenBrowserFunc import OpenBrowser

from function import ChangeInterfaceFunc, ParsingFunc

class Clicked(ParsingFunc.Parsing, ChangeInterfaceFunc.ChangeInterface, QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = ''
        self.tournament = ''


    def clicked_button(self):
        self.ui.ESPNButton.clicked.connect(lambda: OpenBrowser().ESPNSite())
        self.ui.BetboomButton.clicked.connect(lambda: OpenBrowser().BetboomSite())
        self.ui.WinlineButton.clicked.connect(lambda: OpenBrowser().WinlineSite())

        self.ui.RemoveButton.clicked.connect(lambda: self.showMinimized())

        self.ui.FullSizeButton.clicked.connect(lambda: self.normal_or_maximize_window())

        self.ui.NBAButton.clicked.connect(lambda: self.change_tournaments('NBA'))
        self.ui.NHLButton.clicked.connect(lambda: self.change_tournaments('NHL'))
        self.ui.NFLButton.clicked.connect(lambda: self.change_tournaments('NFL'))
        self.ui.MLBButton.clicked.connect(lambda: self.change_tournaments('MLB'))

        self.ui.ParserButton.clicked.connect(lambda: self.change_models('Сбор данных'))
        self.ui.HomeButton.clicked.connect(lambda: self.change_home_page())


    
    def new_button_initialization(self):
        if self.model == 'Сбор данных':
            try:
                self.ui.GetDataButton.clicked.connect(lambda: self.parsing_data())
            except AttributeError:
                pass

            if self.ui.TournamentLabel.text() != 'NFL':
                try:
                    self.ui.DailyDataButton.clicked.connect(lambda: self.daily_parsing_data())
                except AttributeError:
                    pass



    
    # Функции настройки окна
    def normal_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.FullSizeButton.setIcon(QIcon(u":/icon/icon/maximized.svg"))
        else:
            self.showMaximized()
            self.ui.FullSizeButton.setIcon(QIcon(u":/icon/icon/minimized.svg"))



