from datetime import datetime

from server import is_in_the_past


def test_is_in_the_past():
    assert is_in_the_past("2020-XX-22 13:30:00")
    assert is_in_the_past("2020-10-22 13:30:00")
    assert not is_in_the_past("2050-10-22 13:30:00")
    assert is_in_the_past(datetime.now())

    datetime_ = datetime.strptime("2020-10-22 13:30:00", "%Y-%m-%d %H:%M:%S")
    assert is_in_the_past(datetime_)
    datetime_ = datetime.strptime("2050-10-22 13:30:00", "%Y-%m-%d %H:%M:%S")
    assert not is_in_the_past(datetime_)
