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