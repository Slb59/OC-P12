import jwt
import sentry_sdk
from sentry_sdk import capture_exception
from epicevents.views.error import ErrorView
from .session import load_session, read_role
from .config import Environ


def sentry_activate(f):
    def decorator(*args, **kwargs):
        with sentry_sdk.start_transaction(name="epicevent"):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                ErrorView.dsiplay_error_exception(e)
                capture_exception(e)
    return decorator


def is_authenticated(f):
    def decorator(*args, **kwargs):
        token = load_session()
        try:
            env = Environ()
            jwt.decode(token, env.SECRET_KEY, algorithms=['HS256'])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return ErrorView.display_token_expired()
        except jwt.InvalidTokenError:
            return ErrorView.display_token_invalid()
    return decorator


def is_commercial(f):
    def decorator(*args, **kwargs):
        e = args[1]
        if e.role.value == 'Commercial':
            return f(*args, **kwargs)
        else:
            return ErrorView.display_not_commercial()
    return decorator


def is_support(f):
    def decorator(*args, **kwargs):
        e = args[1]
        if e.role.value == 'Support':
            return f(*args, **kwargs)
        else:
            return ErrorView.display_not_support()
    return decorator


def is_manager(f):
    def decorator(*args, **kwargs):
        role = read_role()
        if role == 'Manager':
            return f(*args, **kwargs)
        else:
            return ErrorView.display_not_manager()
    return decorator
