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


















