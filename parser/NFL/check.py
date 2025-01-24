import sqlite3
from parser.NFL.create import сreate

import numpy as np

from parser.utilities.transfer import convert_to_list


def match_bet_check(match_ID):
    try:
        conn = sqlite3.connect(f'database/NFL.db')
        cur = conn.cursor()

        cur.execute(f"SELECT bet.match_ID FROM bet WHERE bet.match_ID = '{match_ID}';")
        inf = cur.fetchall()

        if len(inf) != 0:
            return False
        else:
            return True
    
    except sqlite3.OperationalError:
        сreate()
        return True


def match_check(match_ID):
    try:
        conn = sqlite3.connect(f'database/NFL.db')
        cur = conn.cursor()

        cur.execute(f"SELECT match.match_ID FROM match WHERE match.match_ID = '{match_ID}';")
        inf = cur.fetchall()

        if len(inf) != 0:
            return False
        else:
            return True
    
    except sqlite3.OperationalError:
        сreate()
        return True


def total_check(totals):
    totals.pop(int(len(totals)/2))
    totals.pop(0)

    quarter1_team1 = int(totals[0])
    quarter2_team1 = int(totals[1])
    quarter3_team1 = int(totals[2])
    quarter4_team1 = int(totals[3])
    missed_quarter1_team1 = int(totals[int(len(totals)/2)])
    missed_quarter2_team1 = int(totals[int(len(totals)/2)+1])
    missed_quarter3_team1 = int(totals[int(len(totals)/2)+2])
    missed_quarter4_team1 = int(totals[int(len(totals)/2)+3])
    total_team1 = quarter1_team1 + quarter2_team1 + quarter3_team1 + quarter4_team1

    quarter1_team2 = int(totals[int(len(totals)/2)])
    quarter2_team2 = int(totals[int(len(totals)/2)+1])
    quarter3_team2 = int(totals[int(len(totals)/2)+2])
    quarter4_team2 = int(totals[int(len(totals)/2)+3])
    missed_quarter1_team2 = int(totals[0])
    missed_quarter2_team2 = int(totals[1])
    missed_quarter3_team2 = int(totals[2])
    missed_quarter4_team2 = int(totals[3])
    total_team2 = quarter1_team2 + quarter2_team2 + quarter3_team2 + quarter4_team2

    missed_total_team1 = total_team2
    missed_total_team2 = total_team1

    return [quarter1_team1, missed_quarter1_team1, quarter2_team1, missed_quarter2_team1, quarter3_team1, missed_quarter3_team1, quarter4_team1, missed_quarter4_team1, total_team1, missed_total_team1], [quarter1_team2, missed_quarter1_team2, quarter2_team2, missed_quarter2_team2, quarter3_team2, missed_quarter3_team2, quarter4_team2, missed_quarter4_team2, total_team2, missed_total_team2], [totals[int(len(totals)/2-1)], totals[-1]]


def stage_check(stages):
    if len(stages) == 0:
        game_stage = "regular"
    else:
        stages = [x.lower() for x in stages]
        stages = stages[0].split()

        if 'wild' in stages and 'card' in stages:
            if 'afc' in stages:
                game_stage = "AFC Wild Card Playoffs"
            else:
                game_stage = "NFC Wild Card Playoffs"
        elif 'divisional' in stages:
            if 'afc' in stages:
                game_stage = "AFC Divisional Playoffs"
            else:
                game_stage = "NFC Divisional Playoffs"
        elif 'championship' in stages:
            if 'afc' in stages:
                game_stage = "AFC Championship"
            else:
                game_stage = "NFC Championship"
        elif 'super' in stages and 'bowl' in stages:
            game_stage = "Super Bowl"
        else:
            game_stage = "regular"

        game_stage.lower()

    return game_stage


def check_stat(team1_stat, team2_stat, player_IDs):

    team1_player_stat = list()
    team2_player_stat = list()

    stat_team1 = list()
    stat_team2= list()

    for i in range(10):
        stat_team1.append(team1_stat[i].pop(-1).split(' '))
        stat_team2.append(team2_stat[i].pop(-1).split(' '))


    team1_passing = list()

    if len(team1_stat[0]) != 1:
        for i in range(len(team1_stat[0])):

            if team1_stat[0][0] == "TEAM":
                break
            
            team1_passing.append([])
            team1_passing[i].append(team1_stat[0].pop(0))
            team1_passing[i].append(player_IDs.pop(0))

        for i in range(len(team1_passing)-1, -1, -1):
            stats = team1_stat[0].pop(-1).split(' ')
            team1_passing[i].append([convert_to_list(stat) for stat in stats])

    team2_passing = list()

    if len(team2_stat[0]) != 1:
        for i in range(len(team2_stat[0])):

            if team2_stat[0][0] == "TEAM":
                break
            
            team2_passing.append([])
            team2_passing[i].append(team2_stat[0].pop(0))
            team2_passing[i].append(player_IDs.pop(0))

        for i in range(len(team2_passing)-1, -1, -1):
            stats = team2_stat[0].pop(-1).split(' ')
            team2_passing[i].append([convert_to_list(stat) for stat in stats])

    
    team1_rushing = list()

    if len(team1_stat[1]) != 1:
        for i in range(len(team1_stat[1])):

            if team1_stat[1][0] == "TEAM":
                break
            
            team1_rushing.append([])
            team1_rushing[i].append(team1_stat[1].pop(0))
            team1_rushing[i].append(player_IDs.pop(0))

        for i in range(len(team1_rushing)-1, -1, -1):
            stats = team1_stat[1].pop(-1).split(' ')
            team1_rushing[i].append([convert_to_list(stat) for stat in stats])

    team2_rushing = list()

    if len(team2_stat[1]) != 1:
        for i in range(len(team2_stat[1])):

            if team2_stat[1][0] == "TEAM":
                break
            
            team2_rushing.append([])
            team2_rushing[i].append(team2_stat[1].pop(0))
            team2_rushing[i].append(player_IDs.pop(0))

        for i in range(len(team2_rushing)-1, -1, -1):
            stats = team2_stat[1].pop(-1).split(' ')
            team2_rushing[i].append([convert_to_list(stat) for stat in stats])


    team1_receiving = list()

    if len(team1_stat[2]) != 1:
        for i in range(len(team1_stat[2])):

            if team1_stat[2][0] == "TEAM":
                break
            
            team1_receiving.append([])
            team1_receiving[i].append(team1_stat[2].pop(0))
            team1_receiving[i].append(player_IDs.pop(0))

        for i in range(len(team1_receiving)-1, -1, -1):
            stats = team1_stat[2].pop(-1).split(' ')
            team1_receiving[i].append([convert_to_list(stat) for stat in stats])

    team2_receiving = list()

    if len(team2_stat[2]) != 1:
        for i in range(len(team2_stat[2])):

            if team2_stat[2][0] == "TEAM":
                break
            
            team2_receiving.append([])
            team2_receiving[i].append(team2_stat[2].pop(0))
            team2_receiving[i].append(player_IDs.pop(0))

        for i in range(len(team2_receiving)-1, -1, -1):
            stats = team2_stat[2].pop(-1).split(' ')
            team2_receiving[i].append([convert_to_list(stat) for stat in stats])

    
    team1_fumbles = list()

    if len(team1_stat[3]) != 1:
        for i in range(len(team1_stat[3])):

            if team1_stat[3][0] == "TEAM":
                break
            
            team1_fumbles.append([])
            team1_fumbles[i].append(team1_stat[3].pop(0))
            team1_fumbles[i].append(player_IDs.pop(0))

        for i in range(len(team1_fumbles)-1, -1, -1):
            stats = team1_stat[3].pop(-1).split(' ')
            team1_fumbles[i].append([convert_to_list(stat) for stat in stats])

    team2_fumbles = list()

    if len(team2_stat[3]) != 1:
        for i in range(len(team2_stat[3])):

            if team2_stat[3][0] == "TEAM":
                break
            
            team2_fumbles.append([])
            team2_fumbles[i].append(team2_stat[3].pop(0))
            team2_fumbles[i].append(player_IDs.pop(0))

        for i in range(len(team2_fumbles)-1, -1, -1):
            stats = team2_stat[3].pop(-1).split(' ')
            team2_fumbles[i].append([convert_to_list(stat) for stat in stats])

    
    team1_defense = list()

    if len(team1_stat[4]) != 1:
        for i in range(len(team1_stat[4])):

            if team1_stat[4][0] == "TEAM":
                break
            
            team1_defense.append([])
            team1_defense[i].append(team1_stat[4].pop(0))
            team1_defense[i].append(player_IDs.pop(0))

        for i in range(len(team1_defense)-1, -1, -1):
            stats = team1_stat[4].pop(-1).split(' ')
            team1_defense[i].append([convert_to_list(stat) for stat in stats])

    team2_defense = list()

    if len(team2_stat[4]) != 1:
        for i in range(len(team2_stat[4])):

            if team2_stat[4][0] == "TEAM":
                break
            
            team2_defense.append([])
            team2_defense[i].append(team2_stat[4].pop(0))
            team2_defense[i].append(player_IDs.pop(0))

        for i in range(len(team2_defense)-1, -1, -1):
            stats = team2_stat[4].pop(-1).split(' ')
            team2_defense[i].append([convert_to_list(stat) for stat in stats])


    team1_interceptions = list()

    if len(team1_stat[5]) != 1:
        for i in range(len(team1_stat[5])):

            if team1_stat[5][0] == "TEAM":
                break
            
            team1_interceptions.append([])
            team1_interceptions[i].append(team1_stat[5].pop(0))
            team1_interceptions[i].append(player_IDs.pop(0))

        for i in range(len(team1_interceptions)-1, -1, -1):
            stats = team1_stat[5].pop(-1).split(' ')
            team1_interceptions[i].append([convert_to_list(stat) for stat in stats])

    team2_interceptions = list()

    if len(team2_stat[5]) != 1:
        for i in range(len(team2_stat[5])):

            if team2_stat[5][0] == "TEAM":
                break
            
            team2_interceptions.append([])
            team2_interceptions[i].append(team2_stat[5].pop(0))
            team2_interceptions[i].append(player_IDs.pop(0))

        for i in range(len(team2_interceptions)-1, -1, -1):
            stats = team2_stat[5].pop(-1).split(' ')
            team2_interceptions[i].append([convert_to_list(stat) for stat in stats])

    
    team1_kick_returns = list()

    if len(team1_stat[6]) != 1:
        for i in range(len(team1_stat[6])):

            if team1_stat[6][0] == "TEAM":
                break
            
            team1_kick_returns.append([])
            team1_kick_returns[i].append(team1_stat[6].pop(0))
            team1_kick_returns[i].append(player_IDs.pop(0))

        for i in range(len(team1_kick_returns)-1, -1, -1):
            stats = team1_stat[6].pop(-1).split(' ')
            team1_kick_returns[i].append([convert_to_list(stat) for stat in stats])

    team2_kick_returns = list()

    if len(team2_stat[6]) != 1:
        for i in range(len(team2_stat[6])):

            if team2_stat[6][0] == "TEAM":
                break
            
            team2_kick_returns.append([])
            team2_kick_returns[i].append(team2_stat[6].pop(0))
            team2_kick_returns[i].append(player_IDs.pop(0))

        for i in range(len(team2_kick_returns)-1, -1, -1):
            stats = team2_stat[6].pop(-1).split(' ')
            team2_kick_returns[i].append([convert_to_list(stat) for stat in stats])


    team1_punt_returns = list()

    if len(team1_stat[7]) != 1:
        for i in range(len(team1_stat[7])):

            if team1_stat[7][0] == "TEAM":
                break
            
            team1_punt_returns.append([])
            team1_punt_returns[i].append(team1_stat[7].pop(0))
            team1_punt_returns[i].append(player_IDs.pop(0))

        for i in range(len(team1_punt_returns)-1, -1, -1):
            stats = team1_stat[7].pop(-1).split(' ')
            team1_punt_returns[i].append([convert_to_list(stat) for stat in stats])

    team2_punt_returns = list()

    if len(team2_stat[7]) != 1:
        for i in range(len(team2_stat[7])):

            if team2_stat[7][0] == "TEAM":
                break
            
            team2_punt_returns.append([])
            team2_punt_returns[i].append(team2_stat[7].pop(0))
            team2_punt_returns[i].append(player_IDs.pop(0))

        for i in range(len(team2_punt_returns)-1, -1, -1):
            stats = team2_stat[7].pop(-1).split(' ')
            team2_punt_returns[i].append([convert_to_list(stat) for stat in stats])

    
    team1_kicking = list()

    if len(team1_stat[8]) != 1:
        for i in range(len(team1_stat[8])):

            if team1_stat[8][0] == "TEAM":
                break
            
            team1_kicking.append([])
            team1_kicking[i].append(team1_stat[8].pop(0))
            team1_kicking[i].append(player_IDs.pop(0))

        for i in range(len(team1_kicking)-1, -1, -1):
            stats = team1_stat[8].pop(-1).split(' ')
            team1_kicking[i].append([convert_to_list(stat) for stat in stats])

    team2_kicking = list()

    if len(team2_stat[8]) != 1:
        for i in range(len(team2_stat[8])):

            if team2_stat[8][0] == "TEAM":
                break
            
            team2_kicking.append([])
            team2_kicking[i].append(team2_stat[8].pop(0))
            team2_kicking[i].append(player_IDs.pop(0))

        for i in range(len(team2_kicking)-1, -1, -1):
            stats = team2_stat[8].pop(-1).split(' ')
            team2_kicking[i].append([convert_to_list(stat) for stat in stats])

    
    team1_punting = list()

    if len(team1_stat[9]) != 1:
        for i in range(len(team1_stat[9])):

            if team1_stat[9][0] == "TEAM":
                break
            
            team1_punting.append([])
            team1_punting[i].append(team1_stat[9].pop(0))
            team1_punting[i].append(player_IDs.pop(0))

        for i in range(len(team1_punting)-1, -1, -1):
            stats = team1_stat[9].pop(-1).split(' ')
            team1_punting[i].append([convert_to_list(stat) for stat in stats])

    team2_punting = list()

    if len(team2_stat[9]) != 1:
        for i in range(len(team2_stat[9])):

            if team2_stat[9][0] == "TEAM":
                break
            
            team2_punting.append([])
            team2_punting[i].append(team2_stat[9].pop(0))
            team2_punting[i].append(player_IDs.pop(0))

        for i in range(len(team2_punting)-1, -1, -1):
            stats = team2_stat[9].pop(-1).split(' ')
            team2_punting[i].append([convert_to_list(stat) for stat in stats])


    return stat_team1, stat_team2, \
        team1_passing, team2_passing, \
        team1_rushing, team2_rushing, \
        team1_receiving, team2_receiving, \
        team1_fumbles, team2_fumbles, \
        team1_defense, team2_defense, \
        team1_interceptions, team2_interceptions, \
        team1_kick_returns, team2_kick_returns, \
        team1_punt_returns, team2_punt_returns, \
        team1_kicking, team2_kicking, \
        team1_punting, team2_punting
        

