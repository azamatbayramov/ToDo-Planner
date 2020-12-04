"""Module for working with days of the week"""

import datetime
from all_json import DAYS_OF_THE_WEEK


def get_days_of_the_week_from_string(input_string, language):
    """Get days of the week from string

    Keyword arguments:
    input_string -- string to process
    language -- language for string processing

    If input string is correct:
    Return sorted string with numbers of days
    of the week(Monday - 1, Sunday - 7)
    Else:
    Return False

    Example:
    get_days_of_the_week_from_string("Tuesday Friday", "eng") - "25"
    get_days_of_the_week_from_string("Fr Su We", "eng") - "573"
    get_days_of_the_week_from_string("1 7 3", "eng") - "137"

    get_days_of_the_week_from_string("Tuesday Fr 1", "eng") - False
    get_days_of_the_week_from_string("Fr Fr Fr", "eng") - False
    get_days_of_the_week_from_string("Hello", "eng") - False
    """

    input_string = input_string.lower()
    days_of_the_week = input_string.split()

    # List for numbers of days of the week
    output_list = []

    # Check if days of the week more than in the week
    if len(days_of_the_week) > 7:
        return False

    # Receive different formats of days of the week
    days_of_the_week_int = ['1', '2', '3', '4', '5', '6', '7']
    days_of_the_week_full = DAYS_OF_THE_WEEK["full"][language]
    days_of_the_week_short = DAYS_OF_THE_WEEK["short"][language]

    # Check if all days of the week in integer format
    if all(map(lambda s: s in days_of_the_week_int, days_of_the_week)):
        output_list = list(map(int, days_of_the_week))

    # Check if all days of the week in "full-days" format
    elif all(map(lambda s: s in days_of_the_week_full, days_of_the_week)):
        for day_of_the_week in days_of_the_week:
            output_list.append(
                days_of_the_week_full.index(day_of_the_week)
            )

    # Check if all days of the week in "short-days" format
    elif all(map(lambda s: s in days_of_the_week_short, days_of_the_week)):
        for day_of_the_week in days_of_the_week:
            output_list.append(
                days_of_the_week_short.index(day_of_the_week)
            )

    # Check if the days of the week are repeated
    if output_list != list(set(output_list)):
        return False

    # Sorting all days of the week and converting to the database format
    output_list.sort()
    output_string = ''.join(map(str, output_list))

    return output_string


def get_today_day_of_the_week():
    """Return today's day of the week(Monday - 1, Sunday - 7)"""
    return datetime.datetime.today().weekday() + 1
