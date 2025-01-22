from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import datetime
import time

from parser.NBA.check import check_stat, match_bet_check, match_check, stage_check, total_check
from parser.NBA.save import player_tables, team_stat_pts_tables, team_stat_tables, team_table, bet_predict_tables, bet_old_resul_tables, bet_resul_tables, match_table
from parser.NBA.redact import bet_predict_redact, bet_redact, old_bet_redact


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

        date = datetime.datetime.strptime(self.date_match, '%Y-%m-%d')

        year = date.year

        if date.month >= 10:  # Сезон начинается осенью
            self.season = f"{year}/{int(str(year)[2:]) + 1}"
        else:
            self.season = f"{year - 1}/{str(year)[2:]}"


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

        if not match_bet_check(self.match_ID):
            return 0
        

        teams_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2'))
        )

        teams = list() # Инициируем массив для записи команд

        for team in teams_selenium: # Записываем команды в наш массив
            teams.append(team.get_attribute('textContent'))


        bets_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ubOdK div.Kiog a')) # Собирает название команд
        )

        bets = list() # Инициируем массив для записи команд


        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))

        if len(bets) < 0:
            return 0
        
        bet_predict_tables(self.match_ID, team_table(teams[0], teams[1]), bet_predict_redact(bets))


    def open_matches_link_past(self, link):
        
        self.driver.get(link)

        split_match_ID = link.split('/')
        self.match_ID = split_match_ID[-2]

        if not match_check(self.match_ID):
            return 0

        teams_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Gamestrip__TeamContainer div.Gamestrip__Info div.Gamestrip__InfoWrapper div.ScoreCell__Truncate h2'))
        )

        teams = list() # Инициируем массив для записи команд

        for team in teams_selenium: # Записываем команды в наш массив
            teams.append(team.get_attribute('textContent'))

        self.teams_ID = team_table(teams[0], teams[1])

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
            resul_team1 = 'Win'
            resul_team2 = 'Lose'
        else:
            resul_team2 = 'Win'
            resul_team1 = 'Lose'


        short_names_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Kiog a.mLASH') # Собирает название команд
        
        short_names = list() # Инициируем массив для записи команд

        for short_name in short_names_selenium: # Записываем команды в наш массив
            short_names.append(short_name.get_attribute('textContent'))


        bets_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.ubOdK div.Kiog div.mLASH div') # Собирает название команд

        bets = list() # Инициируем массив для записи команд

        if len(bets_selenium) == 0:
            bets_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.GameInfo__BettingContainer div.betting-details-with-logo div.GameInfo__BettingItem') # Собирает результаты ставок

            bet_function = False
        else:
            bet_function = True

        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))

        if bet_function:
            bet = bet_redact(bets)
        else:
            bet = old_bet_redact(bets, short_names)


        stage = stage_check(stages)

        if stage == 0:
            return 0
        
        total = total_check(totals)

        if len(bets) > 0:
            if bet_function:
                bet_resul_tables(self.match_ID, self.teams_ID, resul_team1, total[-1], bet)
            else:
                bet_old_resul_tables(self.match_ID, self.teams_ID, resul_team1, total[-1], bet)
        
        if not self.open_box_score():
            match_table(self.match_ID, self.teams_ID, self.season, stage, self.date_match)

            team_stat_pts_tables(self.match_ID, self.teams_ID, total)

            return 0

        match_table(self.match_ID, self.teams_ID, self.season, stage, self.date_match)

        team_stat_pts_tables(self.match_ID, self.teams_ID, total)
        team_stat_tables(self.match_ID, self.teams_ID, resul_team1, resul_team2, self.stats[0], self.stats[1])

        player_tables(self.match_ID, self.teams_ID[0], self.stats[2], self.stats[4])
        player_tables(self.match_ID, self.teams_ID[1], self.stats[3], self.stats[5])


    def open_box_score(self):
        
        self.driver.get(f'https://www.espn.com/nba/boxscore/_/gameId/{self.match_ID}')

        playerStat_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex div.Table__ScrollerWrapper div.Table__Scroller table.Table tbody.Table__TBODY tr.Table__TR td.Table__TD') # Собираем стартер команд

        player_stats = list()

        for playerStat in playerStat_selenium: # Записываем стартер команд
            player_stats.append(playerStat.get_attribute('textContent'))


        if len(player_stats) == 0:
            return False

        # time.sleep(2)

        player_link_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="Boxscore Boxscore__ResponsiveWrapper"] div.Wrapper div.Boxscore div.ResponsiveTable div.flex table.Table tbody.Table__TBODY tr[class="Table__TR Table__TR--sm Table__even"] td.Table__TD div.flex a.AnchorLink')) # Собираем игроков команд
        )
        

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

        self.stats = check_stat(player_names, player_stats, player_IDs)

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

        hide_HTML = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main#fittPageContainer')) # Ищем ссылку на скрытый html
        )

        for html in hide_HTML: # Вытаскиваем html код из селениума
            other_HTML = html.get_attribute('outerHTML')

        with open("parser/HTML/sourse_page.html", "w") as file: # Записываем html
            try:
                file.write(other_HTML)
            except UnicodeEncodeError:
                self.driver.refresh() # Если страница не загрузилась полностью, вылаезт ошибка

                time.sleep(10)

                hide_HTML = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main#fittPageContainer')) # Ищем ссылку на скрытый html
                )

                for html in hide_HTML: # Вытаскиваем html код из селениума
                    other_HTML = html.get_attribute('outerHTML')

                with open("parser/HTML/sourse_page.html", "w") as file:
                    file.write(other_HTML)


        with open("parser/HTML/sourse_page.html") as file: # Считываем html
            src = file.read()

        return src
