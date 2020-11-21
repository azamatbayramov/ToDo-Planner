import datetime
from all_json import DAYS_OF_THE_WEEK

# This is a module for working with days of the week


# Function for getting days of the week from a string
def get_days_of_the_week_from_string(input_string, language):
    input_string = input_string.lower()
    output_list = []

    days_of_the_week = input_string.split()

    if len(days_of_the_week) > 7:
        return False

    # Check if all days of the week in integer format
    if all(map(lambda s: s in ['1', '2', '3', '4', '5', '6', '7'], days_of_the_week)):
        output_list = list(map(int, days_of_the_week))

    # Check if all days of the week in "full-days" format
    elif all(map(lambda s: s in DAYS_OF_THE_WEEK["full"][language], days_of_the_week)):
        for day_of_the_week in days_of_the_week:
            output_list.append(DAYS_OF_THE_WEEK["full"][language].index(day_of_the_week))

    # Check if all days of the week in "short-days" format
    elif all(map(lambda s: s in DAYS_OF_THE_WEEK["short"][language], days_of_the_week)):
        for day_of_the_week in days_of_the_week:
            output_list.append(DAYS_OF_THE_WEEK["short"][language].index(day_of_the_week))

    if output_list != list(set(output_list)):
        return False

    # Sorting all days of the week and converting to the database format
    output_list.sort()
    output_string = ''.join(map(str, output_list))

    return output_string


# Function to getting today's day of the week
def today_day_of_the_week():
    return datetime.datetime.today().weekday() + 1
