def symbol_encoder(symbol: str) -> str:
    return symbol.replace('-', '') + "_UMCBL"


def time_frame_encoder(time_frame: int) -> int:
    minute = time_frame // 60
    hour = minute // 60
    day = hour // 24
    week = day // 7
    if minute < 60:
        return "{}m".format(minute)
    elif hour < 6:
        return "{}H".format(hour)
    elif hour < 24:
        return "{}Hutc".format(hour)
    elif day < 7:
        return "{}Duts".format(day)
    elif week < 4:
        return "{}Wutc".format(week)
    else:
        return "1Mutc"


def hedge_mode_encoder(hedge_mode: int) -> str:
    return "single_hold" if 1 == hedge_mode else "double_hold"


def order_side_encoder(order_side: int) -> str:
    return "buy_single" if 1 == order_side else "sell_single"


def order_type_encoder(order_type: int) -> str:
    return "limit" if 1 == order_type else "market"
