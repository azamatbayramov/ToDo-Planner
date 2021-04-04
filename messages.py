"""Module for working with messages texts"""

from emoji import emojize

from all_json import SIGNBOARDS, MESSAGES


# Function for getting signboard for menus and etc
def get_signboard(signboard, language):
    text = SIGNBOARDS[signboard][language]
    emoji = emojize(SIGNBOARDS[signboard]["emoji"], use_aliases=True)
    return emoji + text


# Function for getting messages
def get_message(message, language, emoji=""):
    # Get text and emojize them
    text = emojize(MESSAGES[message][language], use_aliases=True)

    # If have separate emoji, emojize them from text
    if emoji:
        emoji = emojize(emoji, use_aliases=True)
    elif "emoji" in MESSAGES[message]:
        emoji = emojize(MESSAGES[message]["emoji"], use_aliases=True)
    else:
        emoji = ""

    # Return text and emoji
    return emoji + text
