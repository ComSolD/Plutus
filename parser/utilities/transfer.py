def transfer_bet(num):
    if num == 'EVEN':
        return 2.00
    elif int(num) < 0:
        return round(100 / abs(int(num)) + 1, 2)
    else:
        return round(int(num) / 100 + 1, 2)
