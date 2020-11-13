import datetime
import json

CONTENT = json.load(open('content.json', encoding="utf8"))


def get_weekdays_from_str(input_str, language):
    input_str = input_str.lower()
    output_str = ''

    if all(map(lambda s: s in '1234567', input_str.split())):
        weekdays = input_str.split()
        weekdays.sort()
        output_str = ''.join(weekdays)
    elif all(map(lambda s: s in CONTENT["bot"]["weekdays"][language], input_str.split())):
        weekdays = input_str.split()
        for weekday in weekdays:
            output_str += str(CONTENT["bot"]["weekdays"][language].index(weekday))
    elif all(map(lambda s: s in CONTENT["bot"]["short_weekdays"][language], input_str.split())):
        weekdays = input_str.split()
        for weekday in weekdays:
            output_str += str(CONTENT["bot"]["short_weekdays"][language].index(weekday))

    return output_str


def today():
    return datetime.datetime.today().weekday() + 1
