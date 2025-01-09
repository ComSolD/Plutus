import sqlite3
import uuid


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

