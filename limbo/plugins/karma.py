"""!calc <equation> will return the google calculator result for <equation>"""
import re

karma_dict = {}

def update_karma(user, operation):
    karma = karma_dict.setdefault(user, 0)
    bumps = len(operation) - 1

    if operation.startswith('+'):
        karma_dict[user] += bumps
    else:
        karma_dict[user] -= bumps

    return karma_dict[user]

def on_message(msg, server):
    text = msg.get("text", "")

    if text.startswith('!karma'):
        status = []

        for user, karma in karma_dict.items():
            status.append('%s => %s' % (user, karma))

        return '\n'.join(status)

    matches = re.findall(r"([^ +\-@]+)(\+{2,}|-{2,})", text)
    if not matches:
        return

    updates = []

    for match in matches:
        user, operation = match
        karma = update_karma(user, operation)
        updates.append('%s now has %s karma' % (user, karma))

    return '\n'.join(updates)
