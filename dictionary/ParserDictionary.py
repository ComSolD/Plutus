def getDictionary(dictionary: str, key: str) -> str:
    parsers = {'Another': 'Parsing' + key + '(str(self.ui.FirstDate.date().toPyDate()), str(self.ui.SecondDate.date().toPyDate())).date_cycle()',
        'NFL': 'ParsingNFL(year, stage, parser_type).date_cycle()',
    }

    daily = {
        'Daily': 'Parsing' + key + '(str(main_date), str(main_date)).date_cycle()'
    }

    parsers_option ={
        'Wild Card': [1, 3],
        'Divisional Round': [2, 3],
        'Conf. Champ.': [3, 3],
        'Super Bowl': [5,3],
        'Весь сезон': [True],

        'Собрать исходы': 'past',
        'Собрать предикты': 'bet',
    }

    if dictionary == 'parsers':
        if key != 'NFL':
            return parsers.get('Another')
        else:
            return parsers.get('NFL')
    elif dictionary == 'daily':
        return daily.get('Daily')
    else:
        return parsers_option.get(key)
    