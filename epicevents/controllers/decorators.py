import jwt
from epicevents.views.error import (
    display_token_expired, display_token_invalid,
    display_not_commercial,
    display_not_support,
    display_not_manager
)
from .session import load_session
from .config import Environ


def is_authenticated(f):
    def decorator(*args, **kwargs):
        token = load_session()
        try:
            env = Environ()
            jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return display_token_expired()
        except jwt.InvalidTokenError:
            return display_token_invalid()
    return decorator


def is_commercial(f):
    def decorator(*args, **kwargs):
        e = args[1]
        if e.role.value == 'Commercial':
            return f(*args, **kwargs)
        else:
            return display_not_commercial()
    return decorator


def is_support(f):
    def decorator(*args, **kwargs):
        e = args[1]
        if e.role.value == 'Support':
            return f(*args, **kwargs)
        else:
            return display_not_support()
    return decorator


def is_manager(f):
    def decorator(*args, **kwargs):
        e = args[1]
        if e.role.value == 'Manager':
            return f(*args, **kwargs)
        else:
            return display_not_manager()
    return decorator
