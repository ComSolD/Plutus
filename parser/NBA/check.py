import sqlite3
from parser.NBA.create import сreate


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
