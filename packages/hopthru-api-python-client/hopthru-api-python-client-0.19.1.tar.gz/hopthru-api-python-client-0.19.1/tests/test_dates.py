from datetime import date

from hopthru_api_client.dates import last_day_of_month
from hopthru_api_client.dates import last_day_of_week


def test_last_day_of_month():
    assert last_day_of_month(date(2021, 1, 5)) == date(2021, 1, 31)
    assert last_day_of_month(date(2021, 2, 1)) == date(2021, 2, 28)
    assert last_day_of_month(date(2021, 3, 1)) == date(2021, 3, 31)
    assert last_day_of_month(date(2021, 4, 5)) == date(2021, 4, 30)
    assert last_day_of_month(date(2021, 5, 5)) == date(2021, 5, 31)
    assert last_day_of_month(date(2021, 6, 5)) == date(2021, 6, 30)
    assert last_day_of_month(date(2021, 7, 5)) == date(2021, 7, 31)
    assert last_day_of_month(date(2021, 8, 5)) == date(2021, 8, 31)
    assert last_day_of_month(date(2021, 9, 5)) == date(2021, 9, 30)
    assert last_day_of_month(date(2021, 10, 5)) == date(2021, 10, 31)
    assert last_day_of_month(date(2021, 11, 5)) == date(2021, 11, 30)
    assert last_day_of_month(date(2021, 12, 5)) == date(2021, 12, 31)


def test_last_day_of_week():
    assert last_day_of_week(date(2021, 12, 6)) == date(2021, 12, 12)
    assert last_day_of_week(date(2021, 11, 30)) == date(2021, 12, 5)
    assert last_day_of_week(date(2021, 11, 3)) == date(2021, 11, 7)
    assert last_day_of_week(date(2021, 10, 28)) == date(2021, 10, 31)
    assert last_day_of_week(date(2021, 10, 15)) == date(2021, 10, 17)
    assert last_day_of_week(date(2021, 10, 23)) == date(2021, 10, 24)
