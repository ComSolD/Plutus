from parser.utilities.transfer import transfer_bet


def bet_predict_redact(bets):

    win_firstTeam = transfer_bet(bets[1])

    win_secondTeam = transfer_bet(bets[5])

    bet_predict = list()

    bet_predict.append(win_firstTeam)
    bet_predict.append(win_secondTeam)

    bet_predict.append(bets[2][1:-4])
    bet_predict.append(transfer_bet(bets[2][-4] + bets[2][-3] + bets[2][-2] + bets[2][-1]))
    bet_predict.append(transfer_bet(bets[6][-4] + bets[6][-3] + bets[6][-2] + bets[6][-1]))

    bet_predict.append(bets[3][0:-4])
    bet_predict.append(transfer_bet(bets[3][-4] + bets[3][-3] + bets[3][-2] + bets[3][-1]))
    bet_predict.append(bets[7][0:-4])
    bet_predict.append(transfer_bet(bets[7][-4] + bets[7][-3] + bets[7][-2] + bets[7][-1]))

    return bet_predict


def bet_redact(bets):
    bet = list(filter(None, bets))

    for i in range(8):
        bet.pop(0)

    for i in range(8):
        bet.pop(7)

    bet.pop(1)
    bet.pop(3)
    bet.pop(6)
    bet.pop(-3)

    win_firstTeam = transfer_bet(bet[0])

    win_secondTeam = transfer_bet(bet[5])

    bet_predict = list()

    bet_predict.append(win_firstTeam)
    bet_predict.append(win_secondTeam)

    bet_predict.append(bet[1][1:])
    bet_predict.append(transfer_bet(bet[2]))
    bet_predict.append(transfer_bet(bet[-3]))

    bet_predict.append(bet[3])
    bet_predict.append(transfer_bet(bet[4]))
    bet_predict.append(bet[-2])
    bet_predict.append(transfer_bet(bet[-1]))

    return bet_predict


def old_bet_redact(bets, short_names):

    favorite_n_parlay = bets[0].split(' ')

    if favorite_n_parlay[1] == short_names[0]:
        bet_favorite = 'Team1'
    else:
        bet_favorite = 'Team2'

    bet_favorite_parlay = transfer_bet(favorite_n_parlay[2])

    over_n_under_total = bets[1].split(' ')
    
    bet_total = float(over_n_under_total[-1])



    return bet_favorite, bet_favorite_parlay, bet_total