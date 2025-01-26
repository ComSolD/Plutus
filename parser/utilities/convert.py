import re


def convert_to_list(value):
    if '/' in value:
        return list(map(int, value.split('/'))) 
    elif re.search(r'.+-+.', value):
        return list(map(int, value.split('-'))) 
    else:
        return value 