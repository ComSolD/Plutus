import sqlite3


def сreate_mlb():
    conn = sqlite3.connect(f'DataBase/MLB.db')
    cur = conn.cursor()


    # Создание таблицы статистики команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `teamPitchingStat`(teamStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), resul VARCHAR(10), status VARCHAR(10), IP FLOAT, H INTEGER, R INTEGER, ER INTEGER, BB INTEGER, K INTEGER, HR INTEGER, PC INTEGER, ST INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы статистики команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `teamStat`(teamStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), resul VARCHAR(10), status VARCHAR(10), AB FLOAT, R INTEGER, H INTEGER, RBI INTEGER, HR INTEGER, BB INTEGER, K INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы статистики очков команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `teamPTSStat`(teamPTSStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), run INTEGER, runMissed INTEGER, hit INTEGER, hitMissed INTEGER, error INTEGER, inning1 INTEGER, inning1Missed INTEGER, inning2 INTEGER, inning2Missed INTEGER, inning3 INTEGER, inning3Missed INTEGER, inning4 INTEGER, inning4Missed INTEGER, inning5 INTEGER, inning5Missed INTEGER, inning6 INTEGER, inning6Missed INTEGER, inning7 INTEGER, inning7Missed INTEGER, inning8 INTEGER, inning8Missed INTEGER, inning9 INTEGER, inning9Missed INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `player`(player_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()


    # Создание таблицы питчеров
    cur.execute(f"CREATE TABLE IF NOT EXISTS `pitcherPlayerStat`(stat_ID VARCHAR(36) PRIMARY KEY, player_ID VARCHAR(36), match_ID VARCHAR(36), team_ID VARCHAR(36), IP INTEGER, H INTEGER, R INTEGER, ER INTEGER, BB INTEGER, K INTEGER, HR INTEGER, PC INTEGER, ST INTEGER, ERA INTEGER, FOREIGN KEY (player_ID) REFERENCES player (player_ID), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы хиттеров
    cur.execute(f"CREATE TABLE IF NOT EXISTS `hitterPlayerStat`(stat_ID VARCHAR(36) PRIMARY KEY, player_ID VARCHAR(36), match_ID VARCHAR(36), team_ID VARCHAR(36), role VARCHAR(10), AB INTEGER, R INTEGER, H INTEGER, RBI INTEGER, HR INTEGER, BB INTEGER, K INTEGER, AVG FLOAT, OBP FLOAT, SLG FLOAT, FOREIGN KEY (player_ID) REFERENCES player (player_ID), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы бетинга
    cur.execute(f"CREATE TABLE IF NOT EXISTS `bet`(bet_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team1_ID INTEGER, team2_ID INTEGER, \
    \
    ML_team1_parlay FLOAT DEFAULT NULL, ML_team2_parlay FLOAT DEFAULT NULL, ML_resul VARCHAR(36) DEFAULT NULL, total FLOAT, over_total_parlay FLOAT DEFAULT NULL, under_total_parlay FLOAT DEFAULT NULL, total_resul VARCHAR(10) DEFAULT NULL, spread_team1 FLOAT DEFAULT NULL, spread_team1_parlay FLOAT DEFAULT NULL, spread_team2 FLOAT DEFAULT NULL, spread_team2_parlay FLOAT DEFAULT NULL, spread_resul VARCHAR(36), \
    \
    FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы матча
    cur.execute(f"CREATE TABLE IF NOT EXISTS `match`(match_ID VARCHAR(36) PRIMARY KEY, team1_ID INTEGER, team2_ID INTEGER, season VARCHAR(10), stage VARCHAR(20), date DATE, FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы команды
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team`(team_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()

