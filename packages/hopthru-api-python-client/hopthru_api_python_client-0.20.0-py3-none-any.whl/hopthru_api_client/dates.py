import calendar

from datetime import date, timedelta


def last_day_of_month(dt: date) -> date:
    """
    Get the last date of the month for the given date
    :param dt:
    :return:
    """
    last_day_of_month = calendar.monthrange(dt.year, dt.month)[1]
    return dt.replace(day=last_day_of_month)


def last_day_of_week(dt: date) -> date:
    """
    Get the last date of the week for the given date
    :param dt:
    :return:
    """
    start_of_week = dt - timedelta(days=dt.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return end_of_week
