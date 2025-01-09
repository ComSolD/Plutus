from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import numpy as np
import sqlite3

import datetime
import time

import uuid

from parser.NBA.create import сreate
from parser.utilities.transfer import transfer_bet
from parser.NBA.check import match_bet_check
from parser.NBA.save import team_table, bet_predict_tables
from parser.NBA.redact import bet_predict_redact


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
        match_ID = split_match_ID[-2]

        if not match_bet_check(match_ID):
            return 0
        

        teams_selenium = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2'))
        )

        teams = list() # Инициируем массив для записи команд

        for team in teams_selenium: # Записываем команды в наш массив
            teams.append(team.get_attribute('textContent'))


        bets_selenium = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.ubOdK div.Kiog a'))
        )


        bets = list() # Инициируем массив для записи команд


        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))

        if len(bets) < 0:
            return 0
        
        bet_predict_tables(match_ID, team_table(teams[0], teams[1]), bet_predict_redact(bets))


    def open_matches_link_past(self, link):
        
        self.driver.get(link)

        # login_button = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-role="login"]'))
        # )
        # login_button.click()


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

        with open("parser/HTML/sourse_page.html", "w") as file: # Записываем html
            try:
                file.write(other_HTML)
            except UnicodeEncodeError:
                self.driver.refresh() # Если страница не загрузилась полностью, вылаезт ошибка

                time.sleep(10)

                hide_HTML = self.driver.find_elements(By.CSS_SELECTOR, 'main#fittPageContainer') # Ищем ссылку на скрытый html

                for html in hide_HTML: # Вытаскиваем html код из селениума
                    other_HTML = html.get_attribute('outerHTML')

                with open("parser/HTML/sourse_page.html", "w") as file:
                    file.write(other_HTML)


        with open("parser/HTML/sourse_page.html") as file: # Считываем html
            src = file.read()

        return src
