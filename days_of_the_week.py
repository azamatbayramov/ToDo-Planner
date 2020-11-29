import datetime
from all_json import DAYS_OF_THE_WEEK

# This is a module for working with days of the week


def get_days_of_the_week_from_string(input_string, language):
    """Function for getting days of the week from a string"""

    input_string = input_string.lower()
    output_list = []

    days_of_the_week = input_string.split()

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


# Function to getting today's day of the week
def today_day_of_the_week():
    return datetime.datetime.today().weekday() + 1
