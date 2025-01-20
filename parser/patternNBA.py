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




    # Заполнение таблицы

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









