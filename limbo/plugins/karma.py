"""@<user>(++|--) will respectivley increase or decrease karma for <user>"""
import re
import shelve


def bump_karma(user, bumps):
    karma_dict = shelve.open('./karma.shelf')
    key = user.encode('ascii')
    karma = karma_dict.setdefault(key, 0)
    karma += bumps
    karma_dict[key] = karma
    karma_dict.close()
    return user, karma

def update_karma(user, sender, operation):
    bumps = len(operation) - 1

    # Protect limbo from evil doers
    if user == 'limbo' and operation.startswith('-'):
        return bump_karma(sender, -1 * bumps)

    # Can't bump yourself!
    if operation.startswith('+') and user != sender:
        return bump_karma(user, bumps)

    # Everything else is fair game
    return bump_karma(user, -1 * bumps)

def on_message(msg, server):
    text = msg.get("text", "")
    sender = server.slack.server.users.get(msg.get("user"))["name"]

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
        result = update_karma(user, sender, operation)
        status.append('%s now has %s karma' % result)

    return '\n'.join(status)
