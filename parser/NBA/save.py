import sqlite3
import uuid
import logging


def team_table(name_team1, name_team2):
    conn = sqlite3.connect(f'database/NBA.db')
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
    conn = sqlite3.connect(f'database/NBA.db')
    cur = conn.cursor()

    bet_ID = str(uuid.uuid4())

    cur.execute(f"INSERT INTO `bet`(bet_ID, match_ID, team1_ID, team2_ID, ML_team1_parlay, ML_team2_parlay, total, over_total_parlay, under_total_parlay, spread_team1, spread_team1_parlay, spread_team2, spread_team2_parlay) VALUES('{bet_ID}', '{match_id}', '{teams_id[0]}', '{teams_id[1]}', {bet_predict[0]}, {bet_predict[1]}, {bet_predict[2]}, {bet_predict[3]}, {bet_predict[4]}, {bet_predict[5]}, {bet_predict[6]}, {bet_predict[7]}, {bet_predict[8]})")
    conn.commit()


def bet_resul_tables(match_ID, teams, resul_team1, match_total, bet):
    conn = sqlite3.connect(f'database/NBA.db')
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
    conn = sqlite3.connect(f'database/NBA.db')
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
 


def match_table(match_ID, teams, season, stage, date_match):
    conn = sqlite3.connect(f'database/NBA.db')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO `match`(match_ID, team1_ID, team2_ID, season, stage, date) VALUES('{match_ID}', '{teams[0]}', '{teams[1]}', '{season}', '{stage}', '{date_match}')")
    conn.commit()
