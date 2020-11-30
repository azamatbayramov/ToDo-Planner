from emoji import emojize

from all_json import SIGNBOARDS, MESSAGES


def get_signboard(signboard, language):
    text = SIGNBOARDS[signboard][language]
    emoji = emojize(SIGNBOARDS[signboard]["emoji"], use_aliases=True)
    return emoji + text


def get_message(message, language, emoji=""):
    text = emojize(MESSAGES[message][language], use_aliases=True)
    if emoji:
        emoji = emojize(emoji, use_aliases=True)
    elif "emoji" in MESSAGES[message]:
        emoji = emojize(MESSAGES[message]["emoji"], use_aliases=True)
    else:
        emoji = ""

    return emoji + text
