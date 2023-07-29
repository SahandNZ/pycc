from typing import Callable


def param_decorator(func: Callable, param: str, encoder: Callable = None, decoder: Callable = None):
    def inner(*args, **kwargs):
        if encoder is not None and param in kwargs:
            kwargs[param] = encoder(kwargs[param])
        result = func(*args, **kwargs)

        if decoder is not None:
            if isinstance(result, list):
                for item in result:
                    if hasattr(item, '__dict__') and param in item.__dict__:
                        item.__dict__[param] = decoder(item.__dict__[param])
            elif hasattr(result, '__dict__') and param in result.__dict__:
                result.__dict__[param] = decoder(result.__dict__[param])
        return result

    return inner
