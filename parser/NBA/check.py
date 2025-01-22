import sqlite3
from parser.NBA.create import сreate

import numpy as np


def match_bet_check(match_ID):
    try:
        conn = sqlite3.connect(f'database/NBA.db')
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
            conn = sqlite3.connect(f'database/NBA.db')
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

        if 'all-star' in stages:
            return 0
        elif 'rising' in stages and 'stars' in stages:
            return 0
        elif 'makeup' in stages and not 'east' in stages and not 'west' in stages and not 'finals' in stages:
            game_stage = "regular"

        elif 'play-in' in stages and 'east' in stages and '9th' in stages and '10th' in stages:
            game_stage = "play-in east 9th place vs 10th place"
        elif 'play-in' in stages and 'west' in stages and '9th' in stages and '10th' in stages:
            game_stage = "play-in west 9th place vs 10th place"


        elif 'play-in' in stages and 'east' in stages and '7th' in stages and '8th' in stages:
            game_stage = "play-in east 7th place vs 8th place"
        elif 'play-in' in stages and 'west' in stages and '7th' in stages and '8th' in stages:
            game_stage = "play-in west 7th place vs 8th place"

        
        elif 'play-in' in stages and 'east' in stages and '8th' in stages and 'seed' in stages:
            game_stage = "play-in east 8th seed"
        elif 'play-in' in stages and 'west' in stages and '8th' in stages and 'seed' in stages:
            game_stage = "play-in west 8th seed"
        

        elif 'east' in stages and '1st' in stages and 'round' in stages:
            game_stage = "east 1st round"
        elif 'west' in stages and '1st' in stages and 'round' in stages:
            game_stage = "west 1st round"

        elif 'east' in stages and 'semifinals' in stages:
            game_stage = "east semifinals"
        elif 'west' in stages and 'semifinals' in stages:
            game_stage = "west semifinals"

        elif 'east' in stages and 'finals' in stages:
            game_stage = "east finals"
        elif 'west' in stages and 'finals' in stages:
            game_stage = "west finals"

        elif 'nba' in stages and 'finals' in stages:
            game_stage = "nba finals"


        elif 'in-season' in stages and 'group' in stages:
            game_stage = "regular"

        elif 'in-season' in stages and 'quarterfinals' in stages:
            game_stage = "in-season quarterfinals"
        
        elif 'in-season' in stages and 'semifinals' in stages:
            game_stage = "in-season semifinals"

        elif 'in-season' in stages and 'championship' in stages:
            game_stage = "in-season championship"

        else:
            game_stage = "regular"

    return game_stage


def check_stat(player_names, player_stats, player_IDs):
    while('' in player_stats):
        player_stats.remove('')

    num = 0

    redact_list = [[],[],[],[]]

    for i in player_stats:
        if i == 'MIN':
            num += 1
        redact_list[num-1].append(i)
    
    

    for i in range(len(redact_list)):
        redact_list[i].remove('MIN')
        redact_list[i].remove('FG')
        redact_list[i].remove('3PT')
        redact_list[i].remove('FT')
        redact_list[i].remove('OREB')
        redact_list[i].remove('DREB')
        redact_list[i].remove('REB')
        redact_list[i].remove('AST')
        redact_list[i].remove('STL')
        redact_list[i].remove('BLK')
        redact_list[i].remove('TO')
        redact_list[i].remove('PF')
        redact_list[i].remove('+/-')
        redact_list[i].remove('PTS')

    redact_list[3].pop(-3)
    redact_list[3].pop(-2)
    redact_list[3].pop(-1)

    redact_list[1].pop(-3)
    redact_list[1].pop(-2)
    redact_list[1].pop(-1)

    # Общая статистика 1 команды
    stat_team1 = list()

    for stat in range(12):
        stat = redact_list[1].pop(-1)
        stat_team1.append(stat)

    stat_team1.reverse()

    stat_team1[0] = stat_team1[0].split('-')
    stat_team1[1] = stat_team1[1].split('-')
    stat_team1[2] = stat_team1[2].split('-')


    # Общая статистика 2 команды
    stat_team2 = list()

    for stat in range(12):
        stat = redact_list[3].pop(-1)
        stat_team2.append(stat)

    stat_team2.reverse()

    stat_team2[0] = stat_team2[0].split('-')
    stat_team2[1] = stat_team2[1].split('-')
    stat_team2[2] = stat_team2[2].split('-')

    # Редактируем и записывае скамейку 2 команды
    num_DNP = 0

    for DNP in redact_list[3]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[3].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[3] = np.array_split(redact_list[3],len(redact_list[3])/14)

    bench_team2 = list()

    for array in redact_list[3]:
        bench = list(array)
        bench[1] = bench[1].split('-')
        bench[2] = bench[2].split('-')
        bench[3] = bench[3].split('-')
        bench_team2.append(bench)


    for num_player in range(len(bench_team2), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        bench_team2[-num_player].append(player)
        bench_team2[-num_player].append(IDs)


    # Запись данных в массив стартера 2 команды
    num_DNP = 0

    for DNP in redact_list[2]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[2].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[2] = np.array_split(redact_list[2],len(redact_list[2])/14)

    starter_team2 = list()

    for array in redact_list[2]:
        starter = list(array)
        starter[1] = starter[1].split('-')
        starter[2] = starter[2].split('-')
        starter[3] = starter[3].split('-')
        starter_team2.append(starter)


    for num_player in range(len(starter_team2), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        starter_team2[-num_player].append(player)
        starter_team2[-num_player].append(IDs)


    # Редактируем и записывае скамейку 1 команды
    num_DNP = 0

    for DNP in redact_list[1]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[1].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[1] = np.array_split(redact_list[1],len(redact_list[1])/14)

    bench_team1 = list()

    for array in redact_list[1]:
        bench = list(array)
        bench[1] = bench[1].split('-')
        bench[2] = bench[2].split('-')
        bench[3] = bench[3].split('-')
        bench_team1.append(bench)


    for num_player in range(len(bench_team1), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        bench_team1[-num_player].append(player)
        bench_team1[-num_player].append(IDs)

    
    # Запись данных в массив стартера 1 команды
    num_DNP = 0

    for DNP in redact_list[0]:
        if 'DNP' in DNP:
            num_DNP += 1

    if num_DNP > 0:
        for DNP in range(num_DNP):
            redact_list[0].pop(-1)
            player_names.pop(-1)
            player_IDs.pop(-1)

    redact_list[0] = np.array_split(redact_list[0],len(redact_list[0])/14)

    starter_team1 = list()

    for array in redact_list[0]:
        starter = list(array)
        starter[1] = starter[1].split('-')
        starter[2] = starter[2].split('-')
        starter[3] = starter[3].split('-')
        starter_team1.append(starter)


    for num_player in range(len(starter_team1), 0, -1):
        player = player_names.pop(-num_player)
        IDs = player_IDs.pop(-num_player)

        starter_team1[-num_player].append(player)
        starter_team1[-num_player].append(IDs)

    return stat_team1, stat_team2, starter_team1, starter_team2, bench_team1, bench_team2
