import sqlite3
import uuid


def team_table(name_team1, name_team2):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    cur.execute(f"SELECT team_ID FROM `team` WHERE name == '{name_team1}';")

    team1_ID = cur.fetchall()

    if len(team1_ID) == 0:
        team1_ID = str(uuid.uuid4())
        cur.execute(f"INSERT INTO `team`(team_ID, name) VALUES('{team1_ID}', '{name_team1}')")
        conn.commit()
    else:
        team1_ID = team1_ID[0][0]


    cur.execute(f"SELECT team_ID FROM `team` WHERE name == '{name_team2}';")

    team2_ID = cur.fetchall()

    if len(team2_ID) == 0:
        team2_ID = str(uuid.uuid4())
        cur.execute(f"INSERT INTO `team`(team_ID, name) VALUES('{team2_ID}', '{name_team2}')")
        conn.commit()
    else:
        team2_ID = team2_ID[0][0]

    return team1_ID, team2_ID


def bet_predict_tables(match_id, teams_id, bet_predict):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    bet_ID = str(uuid.uuid4())

    cur.execute(f"INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_team1_parlay, ML_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_ID}', '{match_id}', '{teams_id[0]}', '{teams_id[1]}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})")
    conn.commit()


def bet_resul_tables(match_ID, teams, resul_team1, match_total, bet):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()


    cur.execute(f"SELECT bet.match_ID FROM bet WHERE bet.match_ID = '{match_ID}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT bet.total FROM bet WHERE bet.match_ID = '{match_ID}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT bet.spread_team1 FROM bet WHERE bet.match_ID = '{match_ID}';")
        spread = cur.fetchall()[0][0]

        if spread < 0:
            spread_resul = int(match_total[0]) - int(match_total[1]) + spread

            if spread_resul > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_resul = int(match_total[1]) - int(match_total[0]) - spread

            if spread_resul > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]


        cur.execute(f'''UPDATE bet SET ML_resul = '{teams[0] if resul_team1 == "Win" else teams[1]}', total_resul = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_resul = '{spread_team}' WHERE match_ID = '{match_ID}';''')
        conn.commit()

    else:

        bet_ID = str(uuid.uuid4())

        spread = float(bet[5])

        if '-' in bet[5]:
            spread_resul = int(match_total[0]) - int(match_total[1]) + spread

            if spread_resul > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_resul = int(match_total[1]) - int(match_total[0]) - spread

            if spread_resul > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]
            

        cur.execute(f'''INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_team1_parlay, ML_team2_parlay, ML_resul, total, over_total_parlay, under_total_parlay, total_resul, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay, spread_resul) VALUES('{bet_ID}', '{match_ID}', '{teams[0]}', '{teams[1]}', {bet[0]}, {bet[1]},'{teams[0] if resul_team1 == "Win" else teams[1]}', {bet[2]}, {bet[3]}, {bet[4]}, '{'over' if float(bet[2]) < (int(match_total[0]) + int(match_total[1])) else 'under'}', {bet[5]}, {bet[6]}, {bet[7]}, {bet[8]}, '{spread_team}');''')
        conn.commit()


def bet_old_resul_tables(match_ID, teams, resul_team1, match_total, bet):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()


    cur.execute(f"SELECT bet.match_ID FROM bet WHERE bet.match_ID = '{match_ID}';")
    inf = cur.fetchall()

    if len(inf) != 0:
        cur.execute(f"SELECT bet.total FROM bet WHERE bet.match_ID = '{match_ID}';")
        total = cur.fetchall()[0][0]

        cur.execute(f"SELECT bet.spread_team1 FROM bet WHERE bet.match_ID = '{match_ID}';")
        spread = cur.fetchall()[0][0]

        if spread < 0:
            spread_resul = int(match_total[0]) - int(match_total[1]) + spread

            if spread_resul > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]
        else:
            spread_resul = int(match_total[1]) - int(match_total[0]) + spread

            if spread_resul > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]


        cur.execute(f'''UPDATE bet SET ML_resul = '{teams[0] if resul_team1 == "Win" else teams[1]}', total_resul = '{"over" if total < (int(match_total[0]) + int(match_total[1])) else "under"}', spread_resul = '{spread_team}' WHERE match_ID = '{match_ID}';''')
        conn.commit()

    else:

        bet_ID = str(uuid.uuid4())

        if bet[0] == "Team1":
            spread_resul = int(match_total[0]) - int(match_total[1]) + bet[1]

            team1_spread = bet[1]
            team2_spread = abs(bet[1])

            if spread_resul > 0:
                spread_team = teams[0]
            else:
                spread_team = teams[1]

        else:
            spread_resul = int(match_total[1]) - int(match_total[0]) + bet[1]

            team2_spread = bet[1]
            team1_spread = abs(bet[1])

            if spread_resul > 0:
                spread_team = teams[1]
            else:
                spread_team = teams[0]

            
        cur.execute(f'''INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_resul, total, total_resul, spread_team1, spread_team2, spread_resul) VALUES('{bet_ID}', '{match_ID}', '{teams[0]}', '{teams[1]}', '{teams[0] if resul_team1 == "Win" else teams[1]}', {bet[2]}, '{'over' if bet[2] < (int(match_total[0]) + int(match_total[1])) else 'under'}', '{team1_spread}', '{team2_spread}', '{spread_team}');''')
        conn.commit()


def match_table(match_ID, teams_ID, season, game_stage, week_match):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO `match`(match_ID, team1_ID, team2_ID, season, stage, week) VALUES('{match_ID}', '{teams_ID[0]}', '{teams_ID[1]}', '{season}', '{game_stage}', '{week_match}')")
    conn.commit()


def team_stat_pts_tables(match_ID, teams_ID, total):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    # Заполнение таблицы статистики очков команд
    team1_PTS_Stat_ID = str(uuid.uuid4())
    cur.execute(f"INSERT INTO `team_pts_stat`(team_pts_stat_ID, match_ID, team_ID, total, totalMissed, total_Q1, total_Q1Missed, total_Q2, total_Q2Missed, total_Q3, total_Q3Missed, total_Q4, total_Q4Missed) VALUES('{team1_PTS_Stat_ID}', '{match_ID}', '{teams_ID[0]}', {total[0][-2]}, {total[0][-1]}, {total[0][0]}, {total[0][1]}, {total[0][2]}, {total[0][3]}, {total[0][4]}, {total[0][5]}, {total[0][6]}, {total[0][7]})")
    conn.commit()

    team2_PTS_Stat_ID = str(uuid.uuid4())
    cur.execute(f"INSERT INTO `team_pts_stat`(team_pts_stat_ID, match_ID, team_ID, total, totalMissed, total_Q1, total_Q1Missed, total_Q2, total_Q2Missed, total_Q3, total_Q3Missed, total_Q4, total_Q4Missed) VALUES('{team2_PTS_Stat_ID}', '{match_ID}', '{teams_ID[1]}', {total[1][-2]}, {total[1][-1]}, {total[1][0]}, {total[1][1]}, {total[1][2]}, {total[1][3]}, {total[1][4]}, {total[1][5]}, {total[1][6]}, {total[1][7]})")
    conn.commit()


def team_stat_tables(match_ID, teams_ID, resul_team1, resul_team2):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()

    # Заполнение таблицы статистики команд
    team1_Stat_ID = str(uuid.uuid4())
    cur.execute(f"INSERT INTO `team_stat`(team_stat_ID, match_ID, team_ID, resul, status) VALUES('{team1_Stat_ID}', '{match_ID}', '{teams_ID[0]}', '{resul_team1}', 'Away')")
    conn.commit()

    team2_Stat_ID = str(uuid.uuid4()) 
    cur.execute(f"INSERT INTO `team_stat`(team_stat_ID, match_ID, team_ID, resul, status) VALUES('{team2_Stat_ID}', '{match_ID}', '{teams_ID[1]}', '{resul_team2}', 'Home')")
    conn.commit()


def player_tables(match_ID, team_ID, team_passing, team_rushing, team_receiving, team_fumbles, team_defense, team_interceptions, team_kick_returns, team_punt_returns, team_kicking, team_punting):
    conn = sqlite3.connect(f'database/NFL.db')
    cur = conn.cursor()


    if team_passing:
        for player_name in team_passing:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()


            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, C, ATT, YDS, AVG, TD, interception,  SACK, trying_SACK, QBR, RTG) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Passing", {player_name[2][0]}, {player_name[2][1]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7][0]}, {player_name[7][1]}, {player_name[8]}, {player_name[9]})''')
            conn.commit()

    
    if team_rushing:
        for player_name in team_rushing:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, CAR, YDS, AVG, TD, LONG) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Rushing", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()

    
    if team_receiving:
        for player_name in team_receiving:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, REC, YDS, AVG, TD, LONG, TGTS) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Receiving", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]})''')
            conn.commit()

    
    if team_fumbles:
        for player_name in team_fumbles:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, FUM, LOST, REC) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Fumbles", {player_name[2]}, {player_name[3]}, {player_name[4]})''')
            conn.commit()

    
    if team_defense:
        for player_name in team_defense:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, TOT, SOLO, SACKS, TFL, PD, QB_HTS, TD) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Defense", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]}, {player_name[8]})''')
            conn.commit()

    
    if team_interceptions:
        for player_name in team_interceptions:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, interception, YDS, TD) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Fumbles", {player_name[2]}, {player_name[3]}, {player_name[4]})''')
            conn.commit()

    
    if team_kick_returns:
        for player_name in team_kick_returns:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, NO, YDS, AVG, LONG, TD) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Kick Returns", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()
    

    if team_punt_returns:
        for player_name in team_punt_returns:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, NO, YDS, AVG, LONG, TD) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Punt Returns", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]})''')
            conn.commit()

    
    if team_kicking:
        for player_name in team_kicking:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, FG, trying_FG, PCT, LONG, XP, trying_XP, PTS) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Kicking", {player_name[2][0]}, {player_name[2][1]}, {player_name[3]}, {player_name[4]}, {player_name[5][0]}, {player_name[5][1]}, {player_name[6]})''')
            conn.commit()


    if team_punting:
        for player_name in team_punting:

            player_name = player_name[:2] + player_name[2]

            player_ID = player_name[1]

            cur.execute(f'''SELECT player_ID FROM `player` WHERE player_ID == "{player_ID}";''')

            feed_back = cur.fetchall()

            if len(feed_back) == 0:
                cur.execute(f'''INSERT INTO `player`(player_ID, name) VALUES("{player_ID}","{player_name[0]}")''')
                conn.commit()

            stat_ID = str(uuid.uuid4())

            if player_name[0] == '-':
                player_name[0] = 0

            cur.execute(f'''INSERT INTO `player_stat`(stat_ID, player_ID, match_ID, team_ID, position, NO, YDS, AVG, TB, In_20, LONG) VALUES("{stat_ID}", "{player_ID}", "{match_ID}", "{team_ID}", "Punting", {player_name[2]}, {player_name[3]}, {player_name[4]}, {player_name[5]}, {player_name[6]}, {player_name[7]})''')
            conn.commit()


