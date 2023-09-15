import json


def save_session(user, token):
    """
    takes a dictionary user as an argument and serializes it
    in a file called 'session.json'
    """
    user['token'] = token
    with open('session.json', 'w') as f:
        json.dump(user, f, indent=4)


def load_session():
    """
    Open file 'session.json' and read data.
    :raise if no file found return None
    """
    try:
        with open('session.json', 'r') as f:
            session_data = json.load(f)
            return session_data.get('token', None)
    except FileNotFoundError:
        return None
