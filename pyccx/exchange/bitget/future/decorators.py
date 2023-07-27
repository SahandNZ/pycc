def encode_hedge_mode(func):
    def inner(*args, **kwargs):
        kwargs['hedge_mode'] = "single_hold" if 1 == kwargs['hedge_mode'] else "double_hold"
        return func(*args, **kwargs)

    return inner


def encode_symbol(func):
    def inner(*args, **kwargs):
        kwargs['symbol'] = kwargs['symbol'].replace('-', '') + "_UMCBL"
        return func(*args, **kwargs)

    return inner


def encode_order_side(func):
    def inner(*args, **kwargs):
        kwargs['side'] = "buy_single" if 1 == kwargs['side'] else "sell_single"
        return func(*args, **kwargs)

    return inner


def encode_order_type(func):
    def inner(*args, **kwargs):
        kwargs['order_type'] = "limit" if 1 == kwargs['order_type'] else "market"
        return func(*args, **kwargs)

    return inner


def decode_symbol(func):
    def decode(item):
        if item is not None:
            item.__dict__['symbol'] = item.__dict__['symbol'].split('_')[0].replace("USDT", "-USDT")

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner


def decode_order_side(func):
    def decode(item):
        item.__dict__['side'] = 1 if 'buy_single' == item.__dict__['side'] else -1

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner


def decode_order_type(func):
    def decode(item):
        item.__dict__['type'] = 1 if 'limit' == item.__dict__['type'] else 2

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner


def decode_order_status(func):
    def decode(item):
        status = item.__dict__['status']
        if 'new' == status:
            item.__dict__['status'] = 1
        elif 'partially_filled' == status:
            item.__dict__['status'] = 2
        elif 'partially_filled' == status:
            item.__dict__['status'] = 3
        else:
            item.__dict__['status'] = 4

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner


def decode_position_type(func):
    def decode(item):
        if item is not None:
            item.__dict__['type'] = 1 if 'fixed' == item.__dict__['type'] else 2

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner


def decode_position_side(func):
    def decode(item):
        if item is not None:
            item.__dict__['side'] = 1 if 'long' == item.__dict__['side'] else -1

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                decode(item)
            return result
        else:
            decode(result)
            return result

    return inner
