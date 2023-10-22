class TimeFrame:
    MIN1 = 60
    MIN5 = 5 * MIN1
    MIN15 = 15 * MIN1
    MIN30 = 30 * MIN1
    HOUR1 = 60 * MIN1
    HOUR2 = 2 * HOUR1
    HOUR4 = 4 * HOUR1
    HOUR6 = 6 * HOUR1
    HOUR8 = 8 * HOUR1
    HOUR12 = 12 * HOUR1
    DAY1 = 24 * HOUR1
    DAY3 = 3 * DAY1
    WEEK1 = 7 * DAY1
    MONTH1 = 30 * DAY1

    @staticmethod
    def to_str(value: int) -> str:
        minute = value // 60
        hour = minute // 60
        day = hour // 24
        week = day // 7
        if minute < 60:
            return f"{minute} Minute" + ("s" if 1 < minute else "")
        elif hour < 24:
            return f"{hour} Hour" + ("s" if 1 < hour else "")
        elif day < 7:
            return f"{day} Day" + ("s" if 1 < day else "")
        elif week < 4:
            return f"{week} Week" + ("s" if 1 < week else "")
        else:
            return "1 Month"

    @staticmethod
    def from_str(value: str):
        tokens = value.split()
        number = int(tokens[0])
        unit = tokens[1].lower()
        if "minute" in unit:
            return number * TimeFrame.MIN1
        elif "hour" in unit:
            return number * TimeFrame.HOUR1
        elif "day" in unit:
            return number * TimeFrame.DAY1
        elif "week" in unit:
            return number * TimeFrame.WEEK1
        else:
            return TimeFrame.MONTH1
