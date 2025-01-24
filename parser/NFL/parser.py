from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import datetime
import time

from parser.NFL.check import check_stat, match_bet_check, match_check, stage_check, total_check
from parser.NFL.redact import bet_predict_redact, bet_redact, old_bet_redact
from parser.NFL.save import bet_old_resul_tables, bet_predict_tables, bet_resul_tables, match_table, player_tables, team_stat_pts_tables, team_stat_tables, team_table




class ParsingNFL(object):
    def __init__(self, year: str, stage: list, choise_parser: str):
        self.service  = Service(executable_path="parser/drivers/chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_extension("parser/drivers/adblock.crx")
        self.driver = webdriver.Chrome(service = self.service, options=options)
        self.driver.maximize_window()
        self.year = year
        self.stage = stage
        self.choise_parser = choise_parser



    def date_cycle(self):
        year_now = datetime.datetime.today()
        year_now = year_now.strftime('%Y')


        start_week = 1
        start_season_type = 2


        if len(self.stage) == 1:

            print("Im here")

            while True:

                if start_week == 4 and start_season_type == 3:
                    start_week += 1
                    continue
                elif start_week == 6 and start_season_type == 3:
                    return False


                self.url = f"https://www.espn.com/nfl/schedule/_/week/{start_week}/year/{self.year}/seasontype/{start_season_type}"

                self.week_match = start_week

                self.get_matches_link()

                if start_week == 18:
                    start_season_type = 3
                    start_week = 1
                else:
                    start_week += 1
        
        else:
            self.url = f"https://www.espn.com/nfl/schedule/_/week/{self.stage[0]}/year/{self.year}/seasontype/{self.stage[1]}"

            self.week_match = self.stage[1]

            self.get_matches_link()


        self.driver.close()
        self.driver.quit()

        return 'Данные NFL cобраны'
    

    # Сбор всех матчех и проверка их наличия

    def get_matches_link(self):
        self.driver.get(self.url)

        self.season = self.year


        soup = BeautifulSoup(self.work_with_HTML(),'lxml')

        if self.choise_parser == 'bet':
            items_td = soup.find_all("td", class_="date__col Table__TD")

            self.standart_get_data(self.open_matches_link_bet, items_td)

        elif self.choise_parser == 'past':

            items_td = soup.find_all("td", class_="teams__col Table__TD")


            self.standart_get_data(self.open_matches_link_past, items_td)

    
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


        bets_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.ubOdK div.Kiog a') # Собираем данные о ставках

        bets = list() # Инициируем массив для записи команд


        for bet in bets_selenium: # Записываем команды в наш массив
            bets.append(bet.get_attribute('textContent'))

        if len(bets) == 0:
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


        if not self.open_box_score():
            return 0
        
        if len(bets) > 0:
            if bet_function:
                bet_resul_tables(self.match_ID, self.teams_ID, resul_team1, total[-1], bet)
            else:
                bet_old_resul_tables(self.match_ID, self.teams_ID, resul_team1, total[-1], bet)
        
        
        match_table(self.match_ID, self.teams_ID, self.season, stage, self.week_match)

        team_stat_pts_tables(self.match_ID, self.teams_ID, total)
        team_stat_tables(self.match_ID, self.teams_ID, resul_team1, resul_team2)

        player_tables(self.match_ID, self.teams_ID[0], self.stats[2], self.stats[4], self.stats[6], self.stats[8], self.stats[10], self.stats[12], self.stats[14], self.stats[16], self.stats[18], self.stats[20])
        player_tables(self.match_ID, self.teams_ID[1], self.stats[3], self.stats[5], self.stats[7], self.stats[9], self.stats[11], self.stats[13], self.stats[15], self.stats[17], self.stats[19], self.stats[21])


    def open_box_score(self):
        
        self.driver.get(f'https://www.espn.com/nfl/boxscore/_/gameId/{self.match_ID}')

        player_stat_selenium = self.driver.find_elements(By.CSS_SELECTOR, 'div.Boxscore div[class="Wrapper Card__Content"] div.Boxscore__Category') # Собираем статистику

        player_link_selenium = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Boxscore__Athlete a.AnchorLink')) # Собираем ссылку игроков
        )

        player_stats = list()
        player_links = list()


        for stats in player_stat_selenium:
            cells = stats.find_elements(By.CSS_SELECTOR, "div.ResponsiveTable")  # Заполняем данными
            for cell in cells:
                player_stats.append(cell.text)

                
        for i in range(len(player_stats)):  # Редактируем массив
            player_stats[i] = player_stats[i].split('\n')

        cleaned_data = [[item for item in sublist if not item.startswith('#')] for sublist in player_stats]



        for player_link in player_link_selenium: # Записываем ссылки игроков
            player_links.append(player_link.get_attribute('href'))

        player_IDs = list()

        for link in player_links:
            IDs = link.split('/')
            player_IDs.append(IDs[7])

        team1_stat = list()

        team2_stat = list()

        for i in range(10):
            team1_stat.append(cleaned_data.pop(i))

        team2_stat = cleaned_data


        self.stats = check_stat(team1_stat, team2_stat, player_IDs)

        return True


    # Вспомогательные функции

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
