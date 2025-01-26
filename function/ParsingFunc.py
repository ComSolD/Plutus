from interface.MainWindow import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon


class Parsing(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def parsing_data(self):
        self.ui.ParserLabel.setText("")

        from dictionary import ParserDictionary
        from parser.__init___ import ParsingNBA, ParsingNFL, ParsingNHL

        if self.tournament == 'NFL':
            stage = self.ui.StageComboBox.currentText()
            parser_type = ParserDictionary.getDictionary('parsers_option', self.ui.TypeComboBox.currentText())

            if 'Week' in stage:
                get_num = stage.split()

                stage = [int(get_num[-1]), 2]
            else:
                stage = ParserDictionary.getDictionary('parsers_option', self.ui.StageComboBox.currentText())
            

            year = str(self.ui.YearDate.date().toPyDate()).split('-')
            year = year[0]


        parser_func = ParserDictionary.getDictionary('parsers', self.tournament)
        exec(parser_func)
        self.ui.ParserLabel.setText(f'Данные {self.tournament} собраны')


    def daily_parsing_data(self):
        self.ui.ParserLabel.setText("")

        from dictionary import ParserDictionary
        from parser.__init___ import ParsingNBA, ParsingNHL
        import datetime


        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        yesterday = today - datetime.timedelta(days=1)

        parser_func = ParserDictionary.getDictionary('daily', self.tournament)

        main_date = yesterday
        exec(parser_func)

        main_date = today
        exec(parser_func)

        main_date = tomorrow
        exec(parser_func)

        self.ui.ParserLabel.setText(f'Данные {self.tournament} собраны')
