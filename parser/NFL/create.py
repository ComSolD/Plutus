import sqlite3


def сreate():
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    # Создание таблицы статистики команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team_stat`(team_stat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), resul VARCHAR(10), status VARCHAR(10), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()

    # Создание таблицы статистики очков команд
    cur.execute(f"CREATE TABLE IF NOT EXISTS `team_pts_stat`(team_pts_stat_ID VARCHAR(36) PRIMARY KEY, match_ID VARCHAR(36), team_ID VARCHAR(36), total INTEGER, totalMissed INTEGER, total_Q1 INTEGER, total_Q1Missed INTEGER, total_Q2 INTEGER, total_Q2Missed INTEGER, total_Q3 INTEGER, total_Q3Missed INTEGER, total_Q4 INTEGER, total_Q4Missed INTEGER, FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
    conn.commit()

    # Создание таблицы матчей
    cur.execute(f"CREATE TABLE IF NOT EXISTS `match`(match_ID VARCHAR(36) PRIMARY KEY, team1_ID INTEGER, team2_ID INTEGER, season VARCHAR(10), stage VARCHAR(20), week INTEGER, FOREIGN KEY (team1_ID)  REFERENCES team (team_ID), FOREIGN KEY (team2_ID) REFERENCES team (team_ID));")
    conn.commit()


    # Создание таблицы игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `player`(player_ID VARCHAR(36) PRIMARY KEY, name VARCHAR(100));")
    conn.commit()

    # Создание таблицы статистики игроков
    cur.execute(f"CREATE TABLE IF NOT EXISTS `player_stat`(stat_ID VARCHAR(36) PRIMARY KEY, player_ID VARCHAR(36), match_ID VARCHAR(36), team_ID VARCHAR(36), position VARCHAR(10), C INTEGER, ATT INTEGER, YDS INTEGER, AVG FLOAT, TD INTEGER, interception INTEGER,  SACK INTEGER, trying_SACK INTEGER, QBR FLOAT, RTG FLOAT, CAR INTEGER, LONG INTEGER, REC INTEGER, TGTS INTEGER, FUM INTEGER, LOST INTEGER, TOT INTEGER, SOLO INTEGER, SACKS INTEGER, TFL INTEGER, PD INTEGER, QB_HTS INTEGER, NO INTEGER, FG INTEGER, trying_FG INTEGER, PCT INTEGER, XP INTEGER, trying_XP INTEGER, PTS INTEGER, TB INTEGER, In_20 INTEGER, FOREIGN KEY (player_ID) REFERENCES player (player_ID), FOREIGN KEY (match_ID) REFERENCES match (match_ID), FOREIGN KEY (team_ID) REFERENCES team (team_ID));")
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


    # Создание индекса для ускорения соединений и поиска
    cur.execute("CREATE INDEX IF NOT EXISTS idx_team_stat_match_ID ON team_stat(match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_team_stat_team_ID ON team_stat(team_ID);")

    # Для таблицы team_pts_stat
    cur.execute("CREATE INDEX IF NOT EXISTS idx_team_pts_stat_match_ID ON team_pts_stat(match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_team_pts_stat_team_ID ON team_pts_stat(team_ID);")

    # Для таблицы player_stat
    cur.execute("CREATE INDEX IF NOT EXISTS idx_player_stat_match_ID ON player_stat(match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_player_stat_player_ID ON player_stat(player_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_player_stat_team_ID ON player_stat(team_ID);")

    # Для таблицы match
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_date ON match(week);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_team1_ID ON match(team1_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_match_team2_ID ON match(team2_ID);")

    # Для таблицы bet
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_match_ID ON bet(match_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_team1_ID ON bet(team1_ID);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_bet_team2_ID ON bet(team2_ID);")

    # Зафиксировать изменения
    conn.commit()