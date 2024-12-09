import asyncio

from .Action import Action
from .ExtException import ExtException


def prepare_action(f, args, kwargs):
    try:
        name = f'{args[0].__name__}.{f.__name__}'
    except Exception:
        try:
            name = f'{args[0].__class__.__name__}.{f.__name__}'
        except Exception:
            name = f.__name__
    _action = Action(name)
    kwargs['_action'] = _action
    return _action


def async_action(f):
    async def wrapper(*args, **kwargs):
        _action = prepare_action(f, args, kwargs)
        try:
            result = await f(*args, **kwargs)
            if isinstance(result, Action):
                if result != _action:
                    result = _action.add_stat(result)
                    _action.set_end(result)
                else:
                    _action.set_end()
            else:
                _action.set_end(result)
            return _action

        except asyncio.CancelledError as err:
            raise err from err
        except ExtException as err:
            raise ExtException(parent=err, action=_action, skip_traceback=1) from err
        except Exception as err:
            raise ExtException(parent=err, action=_action, skip_traceback=1) from err

    return wrapper


def action(f):
    def wrapper(*args, **kwargs):
        _action = prepare_action(f, args, kwargs)
        try:
            result = f(*args, **kwargs)
            if not isinstance(result, Action):
                _action.set_end(result)
            return _action
        except ExtException as err:
            raise ExtException(parent=err, action=_action, skip_traceback=1) from err
        except Exception as err:
            raise ExtException(parent=err, action=_action, skip_traceback=1) from err

    return wrapper
