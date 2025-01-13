import sqlite3


def сreate_nba():
    conn = sqlite3.connect(f'DataBase/NBA.db')
    cur = conn.cursor()


    # Создание таблицы статистики команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team_stat`(teamStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), resul VARCHAR(10), status VARCHAR(10), FG INTEGER, trying_FG INTEGER, three_PT INTEGER, attempted_three_PT INTEGER, FT INTEGER, trying_FT INTEGER, OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER, turnovers INTEGER, PF INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы статистики очков команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team_pts_stat`(teamPTSStat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), total INTEGER, totalMissed INTEGER, total_Q1 INTEGER, total_Q1Missed INTEGER, total_Q2 INTEGER, total_Q2Missed INTEGER, total_Q3 INTEGER, total_Q3Missed INTEGER, total_Q4 INTEGER, total_Q4Missed INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `player`(player_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()


    # Создание таблицы статистики игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `playerStat`(stat_ID VARCHAR(36) PRIMARY KEY, player_ID VARCHAR(36), match_ID VARCHAR(36), team_ID VARCHAR(36), role VARCHAR(4), status VARCHAR(10), PTS INTEGER, FG INTEGER, trying_FG INTEGER, three_PT INTEGER, attempted_three_PT INTEGER, FT INTEGER, trying_FT INTEGER, OREB INTEGER, DREB INTEGER, REB INTEGER, AST INTEGER, STL INTEGER, BLK INTEGER, turnovers INTEGER, PF INTEGER, plusMinus INTEGER, MIN INTEGER, FOREIGN KEY (player_ID) REFERENCES player (player_ID), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы матчей
    cur.execute(f"CREATE TABLE IF NOT EXISTS `match`(match_ID VARCHAR(36) PRIMARY KEY, team1_ID VARCHAR(36), team2_ID VARCHAR(36), season VARCHAR(10), stage VARCHAR(20), date DATE, FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team`(team_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()


    # Создание таблицы бетинга
    cur.execute(f"CREATE TABLE IF NOT EXISTS `bet`(bet_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team1_ID VARCHAR(36), team2_ID VARCHAR(36), \
    \
    ML_team1_parlay FLOAT DEFAULT NULL, ML_team2_parlay FLOAT DEFAULT NULL, ML_resul VARCHAR(36) DEFAULT NULL, total FLOAT, over_total_parlay FLOAT DEFAULT NULL, under_total_parlay FLOAT DEFAULT NULL, total_resul VARCHAR(10) DEFAULT NULL, spread_team1 FLOAT DEFAULT NULL, spread_team1_parlay FLOAT DEFAULT NULL, spread_team2 FLOAT DEFAULT NULL, spread_team2_parlay FLOAT DEFAULT NULL, spread_resul VARCHAR(36), \
    \
    FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()

    # Создание индекса для ускорения соединений и поиска
    cur.execute("CREATE INDEX IF NOT EXISTS idx_teamStat_match_ID ON teamStat (match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_teamStat_team_ID ON teamStat (team_ID);")

    # Для таблицы teamPTSStat
    cur.execute("CREATE INDEX IF NOT EXISTS idx_teamPTSStat_match_ID ON teamPTSStat (match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_teamPTSStat_team_ID ON teamPTSStat (team_ID);")

    # Для таблицы playerStat
    cur.execute("CREATE INDEX IF NOT EXISTS idx_playerStat_match_ID ON playerStat (match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_playerStat_player_ID ON playerStat (player_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_playerStat_team_ID ON playerStat (team_ID);")

    # Для таблицы match
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_date ON match (date);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_team1_ID ON match (team1_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_team2_ID ON match (team2_ID);")

    # Для таблицы bet
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_match_ID ON bet (match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_team1_ID ON bet (team1_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_team2_ID ON bet (team2_ID);")

    # Зафиксировать изменения
    conn.commit()
