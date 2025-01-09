from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import numpy as np
import sqlite3

import datetime
import time

import uuid

from parser.NBA.create import сreate
from parser.utilities.transfer import transfer_bet


class ParsingNBA(object):
    def __init__(self, first_date, second_date):
        self.service  = Service(executable_path="parser/drivers/chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()
        self.first_date = first_date
        self.second_date = second_date


    def date_cycle(self):
        date_now = datetime.datetime.today()
        date_now = date_now.strftime('%Y-%m-%d')

        start_date = datetime.datetime.strptime(self.first_date, '%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
 
        end_date = datetime.datetime.strptime(self.second_date, '%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
        if start_date < date_now and end_date <= date_now:
            self.choise_parser = 'past'
        elif start_date == date_now and end_date == date_now:
            self.choise_parser = 'today'
        elif start_date >= date_now and end_date > date_now:
            self.choise_parser = 'bet'
        else:
            return "Неверно введены даты"

        while (start_date <= end_date):
            date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            date = date.strftime('%Y%m%d')

            self.url = f"https://www.espn.com/nba/schedule/_/date/{date}"
            self.date_match = start_date

            self.get_matches_link()

            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_date += datetime.timedelta(days=1)
            start_date = start_date.strftime('%Y-%m-%d')

        self.driver.close()
        self.driver.quit()

        return 'Данные NBA cобраны'

            
    # Сбор всех матчех и проверка их наличия

    def get_matches_link(self):
        self.driver.get(self.url)

        time.sleep(5)

        self.season = self.driver.title
        self.season = self.season.split()
        self.season = self.season[3]


        soup = BeautifulSoup(self.work_with_HTML(),'lxml')


        no_games = soup.find_all("section", class_="EmptyTable")


        if len(no_games) != 0:
            no_games_date = no_games[0].find("div").get_text()

            no_games_date = no_games_date.split()

            date_check = datetime.datetime.strptime(self.date_match, '%Y-%m-%d')
            day = date_check.strftime('%#d') + ','
            year = date_check.strftime('%Y')

            if day in no_games_date and year in no_games_date:
                return False


        items_tbody = soup.find("tbody", class_="Table__TBODY")

        if items_tbody == None:
            return 0


        if self.choise_parser == 'bet':
            items_td = items_tbody.find_all("td", class_="date__col Table__TD")

            self.standart_get_data(self.open_matches_link_bet, items_td)

        elif self.choise_parser == 'past':
            items_td = items_tbody.find_all("td", class_="teams__col Table__TD")


            self.standart_get_data(self.open_matches_link_past, items_td)

        else:
            first_td = items_tbody.find_all("td", class_="date__col Table__TD")

            second_td = items_tbody.find_all("td", class_="teams__col Table__TD")

            if len(second_td) == 0:
                items_tbody = items_tbody.find_next("tbody", class_="Table__TBODY")

                second_td = items_tbody.find_all("td", class_="teams__col Table__TD")

            self.exception_get_data(first_td, second_td)


    def open_matches_link_bet(self, link):
              
        self.driver.get(link)

        split_match_ID = link.split('/')
        self.match_ID = split_match_ID[-2]

        if not self.match_bet_check():
            return 0


        try:
            teams_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2') # Собирает название команд

            teams = list() # Инициируем массив для записи команд

            for team in teams_selenium: # Записываем команды в наш массив
                teams.append(team.get_attribute('textContent'))

            self.team_check(teams)
            
        
        except IndexError:
            self.driver.refresh()

            teams_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2') # Собирает название команд

            teams = list() # Инициируем массив для записи команд

            for team in teams_selenium: # Записываем команды в наш массив
                teams.append(team.get_attribute('textContent'))

            self.team_check(teams)


        bets_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.ubOdK div.Kiog a') # Собирает название команд


        bets = list() # Инициируем массив для записи команд


        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))

        if len(bets) < 0:
            return 0

        win_firstTeam = transfer_bet(bets[3])

        win_secondTeam = transfer_bet(bets[7])

        bet_predict = list()

        bet_predict.append(win_firstTeam)
        bet_predict.append(win_secondTeam)

        bet_predict.append(bets[2][1:-4])
        bet_predict.append(transfer_bet(bets[2][-4] + bets[2][-3] + bets[2][-2] + bets[2][-1]))
        bet_predict.append(transfer_bet(bets[6][-4] + bets[6][-3] + bets[6][-2] + bets[6][-1]))

        bet_predict.append(bets[1][0:-4])
        bet_predict.append(transfer_bet(bets[1][-4] + bets[1][-3] + bets[1][-2] + bets[1][-1]))
        bet_predict.append(bets[5][0:-4])
        bet_predict.append(transfer_bet(bets[5][-4] + bets[5][-3] + bets[5][-2] + bets[5][-1]))


        self.team_table()
        self.bet_predict_tables(bet_predict)


    def open_matches_link_past(self, link):
        
        self.driver.get(link)

        split_match_ID = link.split('/')
        self.match_ID = split_match_ID[-2]

        if not self.match_check():
            return 0

        # time.sleep(2)

        try:
            
            teams_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2') # Собирает название команд

            teams = list() # Инициируем массив для записи команд

            for team in teams_selenium: # Записываем команды в наш массив
                teams.append(team.get_attribute('textContent'))

            self.team_check(teams)

        except IndexError:
            self.driver.refresh()

            teams_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2') # Собирает название команд

            teams = list() # Инициируем массив для записи команд

            for team in teams_selenium: # Записываем команды в наш массив
                teams.append(team.get_attribute('textContent'))

            self.team_check(teams)

        # Получение данных через HTML и запись в список
        totals_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Gamestrip__Table div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собирает результаты команд
        stages_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="ScoreCell__GameNote di"]') # Собираем данные об этапе

        totals = list() # Инициируем массив для результата матча
        stages = list() # Инициируем массив для этапа


        for total in totals_selenium: # Записываем итоговый результат
            totals.append(total.get_attribute('textContent'))

        for stage in stages_selenium: # Записываем итоговый результат
            stages.append(stage.get_attribute('textContent'))


        if int(totals[int(len(totals)/2)-1]) > int(totals[-1]):
            self.resul_team1 = 'Win'
            self.resul_team2 = 'Lose'
        else:
            self.resul_team2 = 'Win'
            self.resul_team1 = 'Lose'


        short_names_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Kiog a.mLASH') # Собирает название команд
        
        short_names = list() # Инициируем массив для записи команд

        for short_name in short_names_selenium: # Записываем команды в наш массив
            short_names.append(short_name.get_attribute('textContent'))


        bets_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.GameInfo__BettingContainer div.betting-details-with-logo div.GameInfo__BettingItem') # Собирает название команд

        bets = list() # Инициируем массив для записи команд

        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))


        if self.stage_check(stages) == 0:
            return 0
        self.total_check(totals)
        
        if not self.open_box_score():
            self.team_table()
            self.match_table()
            self.team_stat_tables()

            return 0

        self.team_table()
        self.match_table()
        self.player_tables()
        self.team_stat_tables()

        if len(bets) > 0:
            favorite_n_sprean = bets[0].split(' ')

            if favorite_n_sprean[1] == short_names[0]:
                self.bet_favorite = 'Team1'
            else:
                self.bet_favorite = 'Team2'
            
            self.bet_spread = float(favorite_n_sprean[2])

            over_n_under_total = bets[1].split(' ')
            
            self.bet_total = float(over_n_under_total[-1])
            self.bet_resul_tables()  


    # Заполнение таблицы

    def bet_predict_tables(self, bet_predict):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()

        bet_ID = str(uuid.uuid4())

        cur.execute(f"INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_team1_parlay, ML_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_ID}', '{self.match_ID}', '{self.team1_ID}', '{self.team2_ID}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})")
        conn.commit()


    def bet_resul_tables(self):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()


        cur.execute(f"SELECT bet.match_ID FROM bet WHERE bet.match_ID = '{self.match_ID}';")
        inf = cur.fetchall()

        if len(inf) != 0:
            cur.execute(f"SELECT bet.total FROM bet WHERE bet.match_ID = '{self.match_ID}';")
            total = cur.fetchall()[0][0]

            cur.execute(f"SELECT bet.spread_team1 FROM bet WHERE bet.match_ID = '{self.match_ID}';")
            spread = cur.fetchall()[0][0]

            if spread > 0:
                spread_resul = int(self.total_team1) - int(self.total_team2) + spread
            else:
                spread_resul = int(self.total_team2) - int(self.total_team1) + spread


            cur.execute(f'''UPDATE bet SET ML_resul = '{self.team1_ID if self.resul_team1 == "Win" else self.team2_ID}', total_resul = '{"over" if total < (int(self.total_team1) + int(self.total_team2)) else "under"}', spread_resul = '{self.team1_ID if spread_resul > 0 else self.team2_ID}' WHERE match_ID = '{self.match_ID}';''')
            conn.commit()

        else:

            bet_ID = str(uuid.uuid4())

            if self.bet_favorite == "Team1":
                spread_resul = int(self.total_team1) - int(self.total_team2) + self.bet_spread

                team1_spread = self.bet_spread
                team2_spread = abs(self.bet_spread)
            else:
                spread_resul = int(self.total_team2) - int(self.total_team1) + self.bet_spread

                team2_spread = self.bet_spread
                team1_spread = abs(self.bet_spread)
                
            

            cur.execute(f'''INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_resul, total, total_resul, spread_team1, spread_team2, spread_resul) VALUES('{bet_ID}', '{self.match_ID}', '{self.team1_ID}', '{self.team2_ID}', '{self.team1_ID if self.resul_team1 == "Win" else self.team2_ID}', {self.bet_total}, '{'over' if self.bet_total < (int(self.total_team1) + int(self.missed_total_team1)) else 'under'}', '{team1_spread}', '{team2_spread}', '{self.team1_ID if spread_resul > 0 else self.team2_ID}');''')
            conn.commit()
 

    def team_stat_tables(self):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()

        # Заполнение таблицы статистики команд
        team1_Stat_ID = str(uuid.uuid4())
        cur.execute(f"INSERT INTO `teamStat`(teamStat_ID, match_ID, team_ID, resul, status, FG, tryingFG, '3PT', 'trying3PT', FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, 'TO', PF) VALUES('{team1_Stat_ID}', '{self.match_ID}', '{self.team1_ID}', '{self.resul_team1}', 'Away', {self.stat_team1[0][0]}, {self.stat_team1[0][1]}, {self.stat_team1[1][0]}, {self.stat_team1[1][1]}, {self.stat_team1[2][0]}, {self.stat_team1[2][1]}, {int(self.stat_team1[3])}, {int(self.stat_team1[4])}, {int(self.stat_team1[5])}, {int(self.stat_team1[6])}, {int(self.stat_team1[7])}, {int(self.stat_team1[8])}, {int(self.stat_team1[9])}, {int(self.stat_team1[10])})")
        conn.commit()

        team2_Stat_ID = str(uuid.uuid4()) 
        cur.execute(f"INSERT INTO `teamStat`(teamStat_ID, match_ID, team_ID, resul, status, FG, tryingFG, '3PT', 'trying3PT', FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, 'TO', PF) VALUES('{team2_Stat_ID}', '{self.match_ID}', '{self.team2_ID}', '{self.resul_team2}', 'Home', {self.stat_team2[0][0]}, {self.stat_team2[0][1]}, {self.stat_team2[1][0]}, {self.stat_team2[1][1]}, {self.stat_team2[2][0]}, {self.stat_team2[2][1]}, {int(self.stat_team2[3])}, {int(self.stat_team2[4])}, {int(self.stat_team2[5])}, {int(self.stat_team2[6])}, {int(self.stat_team2[7])}, {int(self.stat_team2[8])}, {int(self.stat_team2[9])}, {int(self.stat_team2[10])})")
        conn.commit()


        # Заполнение таблицы статистики очков команд
        team1_PTS_Stat_ID = str(uuid.uuid4())
        cur.execute(f"INSERT INTO `teamPTSStat`(teamPTSStat_ID, match_ID, team_ID, total, totalMissed, 'total1/4', 'total1/4Missed', 'total2/4', 'total2/4Missed', 'total3/4', 'total3/4Missed', 'total4/4', 'total4/4Missed') VALUES('{team1_PTS_Stat_ID}', '{self.match_ID}', '{self.team1_ID}', {self.total_team1}, {self.missed_total_team1}, {self.quarter1_team1}, {self.missed_quarter1_team1}, {self.quarter2_team1}, {self.missed_quarter2_team1}, {self.quarter3_team1}, {self.missed_quarter3_team1}, {self.quarter4_team1}, {self.missed_quarter4_team1})")
        conn.commit()

        team2_PTS_Stat_ID = str(uuid.uuid4())
        cur.execute(f"INSERT INTO `teamPTSStat`(teamPTSStat_ID, match_ID, team_ID, total, totalMissed, 'total1/4', 'total1/4Missed', 'total2/4', 'total2/4Missed', 'total3/4', 'total3/4Missed', 'total4/4', 'total4/4Missed') VALUES('{team2_PTS_Stat_ID}', '{self.match_ID}', '{self.team2_ID}', {self.total_team2}, {self.missed_total_team2}, {self.quarter1_team2}, {self.missed_quarter1_team2}, {self.quarter2_team2}, {self.missed_quarter2_team2}, {self.quarter3_team2}, {self.missed_quarter3_team2}, {self.quarter4_team2}, {self.missed_quarter4_team2})")
        conn.commit()


    def player_tables(self):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()


        for player_name in self.starter_team1:
            player_ID = player_name[-1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[-2]}")''')
                conn.commit()
 

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `playerStat`(stat_ID, player_ID, match_ID , team_ID , status, PTS, FG, tryingFG, "3PT", "trying3PT", FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, "TO", PF, plusMinus, MIN) VALUES("{stat_ID}", "{player_ID}", "{self.match_ID}", "{self.team1_ID}", "Starter", {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
            conn.commit()


        for player_name in self.starter_team2:
            player_ID = player_name[-1]
            
            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[-2]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `playerStat`(stat_ID, player_ID, match_ID ,team_ID , status, PTS, FG, tryingFG, "3PT", "trying3PT", FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, "TO", PF, plusMinus, MIN) VALUES("{stat_ID}", "{player_ID}", "{self.match_ID}", "{self.team2_ID}", "Starter", {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
            conn.commit()
        

        # Заполнение таблицы игроков скамейки
        for player_name in self.bench_team1:
            player_ID = player_name[-1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[-2]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `playerStat`(stat_ID, player_ID, match_ID ,team_ID , status, PTS, FG, tryingFG, "3PT", "trying3PT", FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, "TO", PF, plusMinus, MIN) VALUES("{stat_ID}", "{player_ID}", "{self.match_ID}", "{self.team1_ID}", "Bench", {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
            conn.commit()


        for player_name in self.bench_team2:
            player_ID = player_name[-1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')


            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[-2]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `playerStat`(stat_ID, player_ID, match_ID ,team_ID , status, PTS, FG, tryingFG, "3PT", "trying3PT", FT, tryingFT, OREB, DREB, REB, AST, STL, BLK, "TO", PF, plusMinus, MIN) VALUES("{stat_ID}", "{player_ID}", "{self.match_ID}", "{self.team2_ID}", "Bench", {player_name[13]}, {player_name[1][0]}, {player_name[1][1]}, {player_name[2][0]}, {player_name[2][1]}, {player_name[3][0]}, {player_name[3][1]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]}, {player_name[9]}, {player_name[10]}, {player_name[11]}, {player_name[12]}, {player_name[0]})''')
            conn.commit()


    def match_table(self):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()

        cur.execute(f"INSERT INTO `match`(match_ID, team1_ID, team2_ID, season, stage, date) VALUES('{self.match_ID}', '{self.team1_ID}', '{self.team2_ID}', '{self.season}', '{self.game_stage}', '{self.date_match}')")
        conn.commit()


    def team_table(self):
        conn = sqlite3.connect(f'database/NBA.db')
        cur = conn.cursor()

        cur.execute(f"SELECT team_ID FROM `team` WHERE name == '{self.name_team1}';")

        self.team1_ID = cur.fetchall()

        if len(self.team1_ID) == 0:
            self.team1_ID = str(uuid.uuid4())
            cur.execute(f"INSERT INTO `team`(team_ID, name) VALUES('{self.team1_ID}', '{self.name_team1}')")
            conn.commit()
        else:
            self.team1_ID = self.team1_ID[0][0]


        cur.execute(f"SELECT team_ID FROM `team` WHERE name == '{self.name_team2}';")

        self.team2_ID = cur.fetchall()

        if len(self.team2_ID) == 0:
            self.team2_ID = str(uuid.uuid4())
            cur.execute(f"INSERT INTO `team`(team_ID, name) VALUES('{self.team2_ID}', '{self.name_team2}')")
            conn.commit()
        else:
            self.team2_ID = self.team2_ID[0][0]
  

    # Проверка данных

    def open_box_score(self):
        
        self.driver.get(f'https://www.espn.com/nba/boxscore/_/gameId/{self.match_ID}')

        playerStat_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собираем стартер команд

        player_stats = list()

        for playerStat in playerStat_selenium: # Записываем стартер команд
            player_stats.append(playerStat.get_attribute('textContent'))


        if len(player_stats) == 0:
            return False

        # time.sleep(2)

        player_link_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex table.Table tbody.Table__TBODY tr[class="Table__TR Table__TR--sm Table__even"] td.Table__TD div.flex a.AnchorLink') # Собираем игроков команд
        

        player_names = list()
        player_links = list()

        for player_link in player_link_selenium: # Записываем стартер команд
            player_names.append(player_link.get_attribute('textContent'))

        for player_link in player_link_selenium: # Записываем стартер команд
            player_links.append(player_link.get_attribute('href'))

        player_IDs = list()
        new_player_name = list()

        for link in player_links:
            IDs = link.split('/')
            player_IDs.append(IDs[7])
            if len(IDs) == 9:
                name = IDs[8].split('-')
                full_name = ''
                for i in range(0, len(name)):
                    full_name += name[i].upper()
                    if i < len(name)-1:
                        full_name += ' '
                new_player_name.append(full_name)

        if len(new_player_name) == len(player_names):
            player_names = new_player_name

        self.check_stat(player_names, player_stats, player_IDs)

        return True


    def check_stat(self, player_names, player_stats, player_IDs):
        while('' in player_stats):
            player_stats.remove('')

        num = 0

        redact_list = [[],[],[],[]]

        for i in player_stats:
            if i == 'MIN':
                num += 1
            redact_list[num-1].append(i)
        
        

        for i in range(len(redact_list)):
            redact_list[i].remove('MIN')
            redact_list[i].remove('FG')
            redact_list[i].remove('3PT')
            redact_list[i].remove('FT')
            redact_list[i].remove('OREB')
            redact_list[i].remove('DREB')
            redact_list[i].remove('REB')
            redact_list[i].remove('AST')
            redact_list[i].remove('STL')
            redact_list[i].remove('BLK')
            redact_list[i].remove('TO')
            redact_list[i].remove('PF')
            redact_list[i].remove('+/-')
            redact_list[i].remove('PTS')

        redact_list[3].pop(-3)
        redact_list[3].pop(-2)
        redact_list[3].pop(-1)

        redact_list[1].pop(-3)
        redact_list[1].pop(-2)
        redact_list[1].pop(-1)

        # Общая статистика 1 команды
        self.stat_team1 = list()

        for stat in range(12):
            stat = redact_list[1].pop(-1)
            self.stat_team1.append(stat)

        self.stat_team1.reverse()

        self.stat_team1[0] = self.stat_team1[0].split('-')
        self.stat_team1[1] = self.stat_team1[1].split('-')
        self.stat_team1[2] = self.stat_team1[2].split('-')


        # Общая статистика 2 команды
        self.stat_team2 = list()

        for stat in range(12):
            stat = redact_list[3].pop(-1)
            self.stat_team2.append(stat)

        self.stat_team2.reverse()

        self.stat_team2[0] = self.stat_team2[0].split('-')
        self.stat_team2[1] = self.stat_team2[1].split('-')
        self.stat_team2[2] = self.stat_team2[2].split('-')

        # Редактируем и записывае скамейку 2 команды
        num_DNP = 0

        for DNP in redact_list[3]:
            if 'DNP' in DNP:
                num_DNP += 1

        if num_DNP > 0:
            for DNP in range(num_DNP):
                redact_list[3].pop(-1)
                player_names.pop(-1)
                player_IDs.pop(-1)

        redact_list[3] = np.array_split(redact_list[3],len(redact_list[3])/14)

        self.bench_team2 = list()

        for array in redact_list[3]:
            bench = list(array)
            bench[1] = bench[1].split('-')
            bench[2] = bench[2].split('-')
            bench[3] = bench[3].split('-')
            self.bench_team2.append(bench)


        for num_player in range(len(self.bench_team2), 0, -1):
            player = player_names.pop(-num_player)
            IDs = player_IDs.pop(-num_player)

            self.bench_team2[-num_player].append(player)
            self.bench_team2[-num_player].append(IDs)


        # Запись данных в массив стартера 2 команды
        num_DNP = 0

        for DNP in redact_list[2]:
            if 'DNP' in DNP:
                num_DNP += 1

        if num_DNP > 0:
            for DNP in range(num_DNP):
                redact_list[2].pop(-1)
                player_names.pop(-1)
                player_IDs.pop(-1)

        redact_list[2] = np.array_split(redact_list[2],len(redact_list[2])/14)

        self.starter_team2 = list()

        for array in redact_list[2]:
            starter = list(array)
            starter[1] = starter[1].split('-')
            starter[2] = starter[2].split('-')
            starter[3] = starter[3].split('-')
            self.starter_team2.append(starter)


        for num_player in range(len(self.starter_team2), 0, -1):
            player = player_names.pop(-num_player)
            IDs = player_IDs.pop(-num_player)

            self.starter_team2[-num_player].append(player)
            self.starter_team2[-num_player].append(IDs)


        # Редактируем и записывае скамейку 1 команды
        num_DNP = 0

        for DNP in redact_list[1]:
            if 'DNP' in DNP:
                num_DNP += 1

        if num_DNP > 0:
            for DNP in range(num_DNP):
                redact_list[1].pop(-1)
                player_names.pop(-1)
                player_IDs.pop(-1)

        redact_list[1] = np.array_split(redact_list[1],len(redact_list[1])/14)

        self.bench_team1 = list()

        for array in redact_list[1]:
            bench = list(array)
            bench[1] = bench[1].split('-')
            bench[2] = bench[2].split('-')
            bench[3] = bench[3].split('-')
            self.bench_team1.append(bench)


        for num_player in range(len(self.bench_team1), 0, -1):
            player = player_names.pop(-num_player)
            IDs = player_IDs.pop(-num_player)

            self.bench_team1[-num_player].append(player)
            self.bench_team1[-num_player].append(IDs)

        
        # Запись данных в массив стартера 1 команды
        num_DNP = 0

        for DNP in redact_list[0]:
            if 'DNP' in DNP:
                num_DNP += 1

        if num_DNP > 0:
            for DNP in range(num_DNP):
                redact_list[0].pop(-1)
                player_names.pop(-1)
                player_IDs.pop(-1)

        redact_list[0] = np.array_split(redact_list[0],len(redact_list[0])/14)

        self.starter_team1 = list()

        for array in redact_list[0]:
            starter = list(array)
            starter[1] = starter[1].split('-')
            starter[2] = starter[2].split('-')
            starter[3] = starter[3].split('-')
            self.starter_team1.append(starter)


        for num_player in range(len(self.starter_team1), 0, -1):
            player = player_names.pop(-num_player)
            IDs = player_IDs.pop(-num_player)

            self.starter_team1[-num_player].append(player)
            self.starter_team1[-num_player].append(IDs)


    def team_check(self, teams):
        self.name_team1 = teams[0]
    
        self.name_team2 = teams[1]


    def total_check(self, totals):
        totals.pop(int(len(totals)/2))
        totals.pop(0)

        self.quarter1_team1 = int(totals[0])
        self.quarter2_team1 = int(totals[1])
        self.quarter3_team1 = int(totals[2])
        self.quarter4_team1 = int(totals[3])
        self.missed_quarter1_team1 = int(totals[int(len(totals)/2)])
        self.missed_quarter2_team1 = int(totals[int(len(totals)/2)+1])
        self.missed_quarter3_team1 = int(totals[int(len(totals)/2)+2])
        self.missed_quarter4_team1 = int(totals[int(len(totals)/2)+3])
        self.total_team1 = self.quarter1_team1 + self.quarter2_team1 + self.quarter3_team1 + self.quarter4_team1

        self.quarter1_team2 = int(totals[int(len(totals)/2)])
        self.quarter2_team2 = int(totals[int(len(totals)/2)+1])
        self.quarter3_team2 = int(totals[int(len(totals)/2)+2])
        self.quarter4_team2 = int(totals[int(len(totals)/2)+3])
        self.missed_quarter1_team2 = int(totals[0])
        self.missed_quarter2_team2 = int(totals[1])
        self.missed_quarter3_team2 = int(totals[2])
        self.missed_quarter4_team2 = int(totals[3])
        self.total_team2 = self.quarter1_team2 + self.quarter2_team2 + self.quarter3_team2 + self.quarter4_team2

        self.missed_total_team1 = self.total_team2
        self.missed_total_team2 = self.total_team1


    def stage_check(self, stages):
        if len(stages) == 0:
            self.game_stage = "regular"
        else:
            stages = [x.lower() for x in stages]
            stages = stages[0].split()

            if 'all-star' in stages:
                return 0
            elif 'rising' in stages and 'stars' in stages:
                return 0
            elif 'makeup' in stages and not 'east' in stages and not 'west' in stages and not 'finals' in stages:
                self.game_stage = "regular"

            elif 'play-in' in stages and 'east' in stages and '9th' in stages and '10th' in stages:
                self.game_stage = "play-in east 9th place vs 10th place"
            elif 'play-in' in stages and 'west' in stages and '9th' in stages and '10th' in stages:
                self.game_stage = "play-in west 9th place vs 10th place"


            elif 'play-in' in stages and 'east' in stages and '7th' in stages and '8th' in stages:
                self.game_stage = "play-in east 7th place vs 8th place"
            elif 'play-in' in stages and 'west' in stages and '7th' in stages and '8th' in stages:
                self.game_stage = "play-in west 7th place vs 8th place"

            
            elif 'play-in' in stages and 'east' in stages and '8th' in stages and 'seed' in stages:
                self.game_stage = "play-in east 8th seed"
            elif 'play-in' in stages and 'west' in stages and '8th' in stages and 'seed' in stages:
                self.game_stage = "play-in west 8th seed"
            

            elif 'east' in stages and '1st' in stages and 'round' in stages:
                self.game_stage = "east 1st round"
            elif 'west' in stages and '1st' in stages and 'round' in stages:
                self.game_stage = "west 1st round"

            elif 'east' in stages and 'semifinals' in stages:
                self.game_stage = "east semifinals"
            elif 'west' in stages and 'semifinals' in stages:
                self.game_stage = "west semifinals"

            elif 'east' in stages and 'finals' in stages:
                self.game_stage = "east finals"
            elif 'west' in stages and 'finals' in stages:
                self.game_stage = "west finals"

            elif 'nba' in stages and 'finals' in stages:
                self.game_stage = "nba finals"


            elif 'in-season' in stages and 'group' in stages:
                self.game_stage = "regular"

            elif 'in-season' in stages and 'quarterfinals' in stages:
                self.game_stage = "in-season quarterfinals"
            
            elif 'in-season' in stages and 'semifinals' in stages:
                self.game_stage = "in-season semifinals"

            elif 'in-season' in stages and 'championship' in stages:
                self.game_stage = "in-season championship"

            else:
                self.game_stage = "regular"


    def match_bet_check(self):

        try:
            conn = sqlite3.connect(f'database/NBA.db')
            cur = conn.cursor()

            cur.execute(f"SELECT bet.match_ID FROM bet WHERE bet.match_ID = '{self.match_ID}';")
            inf = cur.fetchall()

            if len(inf) != 0:
                return False
            else:
                return True
        
        except sqlite3.OperationalError:
            сreate()
            return True


    def match_check(self):

        try:
            conn = sqlite3.connect(f'database/NBA.db')
            cur = conn.cursor()

            cur.execute(f"SELECT match.match_ID FROM match WHERE match.match_ID = '{self.match_ID}';")
            inf = cur.fetchall()

            if len(inf) != 0:
                return False
            else:
                return True
        
        except sqlite3.OperationalError:
            сreate()
            return True


    # Вспомогательные функции

    def exception_get_data(self, first_td, second_td):

        matches = list()

        for td in first_td:
            if len(td) > 0 and td.find("a").get_text() != 'Postponed' and td.find("a").get_text() != 'Canceled':
                matches.append(td.find("a").get("href"))

        for match in matches:
            try:
                self.open_matches_link_bet("https://www.espn.com" + match)
            except IndexError:
                self.driver.refresh()
                self.open_matches_link_bet("https://www.espn.com" + match)


        matches = list()


        matches = list()

        for td in second_td:
            if len(td) > 0 and td.find("a").get_text() != 'Postponed' and td.find("a").get_text() != 'Canceled':
                matches.append(td.find("a").get("href"))

        for match in matches:
            try:
                self.open_matches_link_past("https://www.espn.com" + match)
            except IndexError:
                self.driver.refresh()
                self.open_matches_link_past("https://www.espn.com" + match)


    def standart_get_data(self, working_func, items_td):

        matches = list()

        for td in items_td:
            if len(td) > 0 and td.find("a").get_text() != 'Postponed' and td.find("a").get_text() != 'Canceled':
                matches.append(td.find("a").get("href"))

        
        for match in matches:
            try:
                working_func("https://www.espn.com" + match)
            except IndexError:
                self.driver.refresh()
                working_func("https://www.espn.com" + match)


    def work_with_HTML(self):
        hide_HTML = self.driver.find_elements(By.CSS_SELECTOR, 'main#fittPageContainer') # Ищем ссылку на скрытый html

        for html in hide_HTML: # Вытаскиваем html код из селениума
            other_HTML = html.get_attribute('outerHTML')

        with open("Parser/HTML/sourse_page.html", "w") as file: # Записываем html
            try:
                file.write(other_HTML)
            except UnicodeEncodeError:
                self.driver.refresh() # Если страница не загрузилась полностью, вылаезт ошибка

                time.sleep(10)

                hide_HTML = self.driver.find_elements(By.CSS_SELECTOR, 'main#fittPageContainer') # Ищем ссылку на скрытый html

                for html in hide_HTML: # Вытаскиваем html код из селениума
                    other_HTML = html.get_attribute('outerHTML')

                with open("Parser/HTML/sourse_page.html", "w") as file:
                    file.write(other_HTML)


        with open("Parser/HTML/sourse_page.html") as file: # Считываем html
            src = file.read()

        return src



