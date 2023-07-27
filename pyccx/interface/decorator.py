from collections import Callable


def param_decorator(func: Callable, param: str, encoder: Callable = None, decoder: Callable = None):
    def inner(*args, **kwargs):
        if encoder is not None:
            kwargs[param] = encoder(kwargs[param])
        result = func(*args, **kwargs)
        if decoder is not None:
            if isinstance(result, list):
                for item in result:
                    if param in item.__dict__:
                        item.__dict__[param] = decoder(item.__dict__[param])
            elif param in result.__dict__:
                result.__dict__[param] = decoder(result.__dict__[param])
        return result

    return inner
