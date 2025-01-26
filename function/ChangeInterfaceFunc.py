from interface.MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon

from interface import HomeInterface, ParserInterface, NFLParserInterface

class ChangeInterface(NFLParserInterface.Interface, ParserInterface.Interface, HomeInterface.Interface, QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = ''
        self.tournament = ''


    def change_home_page(self):
        try:
            self.old_tournament.setStyleSheet("background-color: #501F3A;")
        except AttributeError:
            pass

        try:
            self.old_model.setStyleSheet("background-color: #501F3A;")

            for i in range(self.MainWidget.count()-1, 0-1, -1):
                self.MainWidget.itemAt(i).widget().setParent(None)

        except AttributeError:
            for i in range(self.MainWidget.count()-1, 0-1, -1):
                self.MainWidget.itemAt(i).widget().setParent(None)

        self.ui.TournamentLabel.setText('Страница')
        self.ui.ModelLabel.setText('Домашняя')


        self.model = ''

        self.tournament = ''

        self.FirstTime = True
            
        self.callHomeInterface()


    def change_tournaments(self, tournament):
        self.ui.TournamentLabel.setText(tournament)

        try:
            self.old_tournament.setStyleSheet("background-color: #501F3A;")
        except AttributeError:
            pass
        


        if self.tournament == 'NFL' and self.tournament != tournament and self.model == 'Сбор данных':
            for i in range(self.MainWidget.count()-1, 0-1, -1):
                    self.MainWidget.itemAt(i).widget().setParent(None)
            self.callParserInterface()
            self.new_button_initialization()

        
        elif self.tournament != 'NFL' and tournament == 'NFL' and self.model == 'Сбор данных':
            for i in range(self.MainWidget.count()-1, 0-1, -1):
                    self.MainWidget.itemAt(i).widget().setParent(None)
            self.callNFLParserInterface()
            self.new_button_initialization()
            

        tournament_button = {
            'NBA': self.ui.NBAButton,
            'MLB': self.ui.MLBButton,
            'NFL': self.ui.NFLButton,
            'NHL': self.ui.NHLButton,
        }

        self.old_tournament = tournament_button[tournament]

        self.old_tournament.setStyleSheet("background-color: #CB2D6F;")

        self.tournament = tournament

        if self.model == '':
            self.change_models('Сбор данных')


    def change_models(self, model):
        self.ui.ModelLabel.setText(model)

        try:
            self.old_model.setStyleSheet("background-color: #501F3A;")

            if self.old_model != model:
                for i in range(self.MainWidget.count()-1, 0-1, -1):
                    self.MainWidget.itemAt(i).widget().setParent(None)
        except AttributeError:
            for i in range(self.MainWidget.count()-1, 0-1, -1):
                    self.MainWidget.itemAt(i).widget().setParent(None)
        

        model_button = {
            'Сбор данных': self.ui.ParserButton,
        }

        self.old_model = model_button[model]

        self.old_model.setStyleSheet("background-color: #CB2D6F;")

        self.model = model


        if self.tournament != 'NFL':
            self.callParserInterface()
        else:
            self.callNFLParserInterface()

        self.new_button_initialization()
        self.value_tournament = ''

        
        if self.tournament == '':
            self.change_tournaments('NBA')