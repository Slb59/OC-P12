import json


def save_session(user, token):
    """
    takes a dictionary user as an argument and serializes it
    in a file called 'session.json'
    """
    user['token'] = token
    with open('session.json', 'w') as f:
        json.dump(user, f, indent=4)
