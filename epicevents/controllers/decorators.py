import jwt
from epicevents.views.error import display_token_expired, display_token_invalid
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
