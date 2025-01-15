from parser.utilities.transfer import transfer_bet


def bet_predict_redact(bets):
    win_firstTeam = transfer_bet(bets[3])

    win_secondTeam = transfer_bet(bets[7])

    bet_predict = list()

    bet_predict.append(win_firstTeam)
    bet_predict.append(win_secondTeam)

    bet_predict.append(bets[2][1:-4])
    bet_predict.append(transfer_bet(bets[2][-4] + bets[2][-3] + bets[2][-2] + bets[2][-1]))
    bet_predict.append(transfer_bet(bets[6][-4] + bets[6][-3] + bets[6][-2] + bets[6][-1]))

    bet_predict.append(bets[1][0:-4])
    bet_predict.append(transfer_bet(bets[1][-4] + bets[1][-3] + bets[1][-2] + bets[1][-1]))
    bet_predict.append(bets[5][0:-4])
    bet_predict.append(transfer_bet(bets[5][-4] + bets[5][-3] + bets[5][-2] + bets[5][-1]))

    return bet_predict


def bet_redact(bets):

    bet = list(filter(None, bets))

    for i in range(8):
        bet.pop(0)

    for i in range(9):
        bet.pop(6)

    bet.pop(2)
    bet.pop(-1)
    bet.pop(-4)

    win_firstTeam = transfer_bet(bet[4])

    win_secondTeam = transfer_bet(bet[-1])

    bet_predict = list()

    bet_predict.append(win_firstTeam)
    bet_predict.append(win_secondTeam)

    bet_predict.append(bet[2][1:6])
    bet_predict.append(transfer_bet(bet[3][-4] + bet[3][-3] + bet[3][-2] + bet[3][-1]))
    bet_predict.append(transfer_bet(bet[-2][-4] + bet[-2][-3] + bet[-2][-2] + bet[-2][-1]))

    bet_predict.append(bet[0])
    bet_predict.append(transfer_bet(bet[1][-4] + bet[1][-3] + bet[1][-2] + bet[1][-1]))
    bet_predict.append(bet[5])
    bet_predict.append(transfer_bet(bet[6][-4] + bet[6][-3] + bet[6][-2] + bet[6][-1]))

    return bet_predict


def old_bet_redact(bets, short_names):
    favorite_n_sprean = bets[0].split(' ')

    if favorite_n_sprean[1] == short_names[0]:
        bet_favorite = 'Team1'
    else:
        bet_favorite = 'Team2'
    
    bet_spread = float(favorite_n_sprean[2])

    over_n_under_total = bets[1].split(' ')
    
    bet_total = float(over_n_under_total[-1])


    return bet_favorite, bet_spread, bet_total