"""!calc <equation> will return the google calculator result for <equation>"""
import re
import shelve


def update_karma(user, sender, operation):
    karma_dict = shelve.open('./karma.shelf')
    key = user.encode('ascii')
    karma = karma_dict.setdefault(key, 0)
    bumps = len(operation) - 1

    if operation.startswith('+') and user != sender:
        karma += bumps
    else:
        karma -= bumps

    karma_dict[key] = karma
    karma_dict.close()

    return karma

def on_message(msg, server):
    text = msg.get("text", "")

    status = []

    if text.startswith('!karma'):

        karma_dict = shelve.open('./karma.shelf')
        for user, karma in karma_dict.items():
            status.append('%s => %s' % (user, karma))

        karma_dict.close()
        return '\n'.join(status)

    matches = re.findall(r"@([^ +\-@]+)\>(\+{2,}|-{2,})", text)
    if not matches:
        return

    for user_id, operation in matches:
        user = server.slack.server.users.get(user_id)["name"]
        sender = server.slack.server.users.get(msg.get("user"))["name"]
        karma = update_karma(user, sender, operation)
        status.append('%s now has %s karma' % (user, karma))

    return '\n'.join(status)
