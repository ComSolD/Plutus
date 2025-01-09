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

