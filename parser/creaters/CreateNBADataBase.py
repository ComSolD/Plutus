import sqlite3


def сreate_nba():
    conn = sqlite3.connect(f'DataBase/NBA.db')
    cur = conn.cursor()


    # Создание таблицы статистики команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `teamStat`(teamStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), resul VARCHAR(10), status VARCHAR(10), FG INTEGER, tryingFG INTEGER, '3PT' INTEGER, 'trying3PT' INTEGER, FT INTEGER, tryingFT INTEGER, OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER, 'TO' INTEGER, PF INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы статистики очков команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `teamPTSStat`(teamPTSStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), total INTEGER, totalMissed INTEGER, 'total1/4' INTEGER, 'total1/4Missed' INTEGER, 'total2/4' INTEGER, 'total2/4Missed' INTEGER, 'total3/4' INTEGER, 'total3/4Missed' INTEGER, 'total4/4' INTEGER, 'total4/4Missed' INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `player`(player_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()


    # Создание таблицы статистики игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `playerStat`(stat_ID VARCHAR(36) PRIMARY KEY, player_ID VARCHAR(36), match_ID VARCHAR(36), team_ID VARCHAR(36), role VARCHAR(4), status VARCHAR(10), PTS INTEGER, FG INTEGER, tryingFG INTEGER, '3PT' INTEGER, 'trying3PT' INTEGER, FT INTEGER, tryingFT INTEGER, OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER, 'TO' INTEGER, PF INTEGER, plusMinus INTEGER, MIN INTEGER, FOREIGN KEY (player_ID) REFERENCES player (player_ID), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы матчей
    cur.execute(f"CREATE TABLE IF NOT EXISTS `match`(match_ID VARCHAR(36) PRIMARY KEY, team1_ID INTEGER, team2_ID INTEGER, season VARCHAR(10), stage VARCHAR(20), date DATE, FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team`(team_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()


    # Создание таблицы бетинга
    cur.execute(f"CREATE TABLE IF NOT EXISTS `bet`(bet_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team1_ID INTEGER, team2_ID INTEGER, \
    \
    ML_team1_parlay FLOAT DEFAULT NULL, ML_team2_parlay FLOAT DEFAULT NULL, ML_resul VARCHAR(36) DEFAULT NULL, total FLOAT, over_total_parlay FLOAT DEFAULT NULL, under_total_parlay FLOAT DEFAULT NULL, total_resul VARCHAR(10) DEFAULT NULL, spread_team1 FLOAT DEFAULT NULL, spread_team1_parlay FLOAT DEFAULT NULL, spread_team2 FLOAT DEFAULT NULL, spread_team2_parlay FLOAT DEFAULT NULL, spread_resul VARCHAR(36), \
    \
    FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()