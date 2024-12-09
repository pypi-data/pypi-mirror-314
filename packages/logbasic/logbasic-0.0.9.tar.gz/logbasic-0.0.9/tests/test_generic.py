from src import logbasic
import datetime as dt


def test_debug():
    logbasic.debug('help')


def test_format_datetime():
    assert logbasic.format_datetime(dt.datetime(2024, 1, 1, 1, 1, 1, 1)) == 'Mon, 01 Jan 2024, 01:01:01.00'


def test_format_datetime_utc():
    assert logbasic.format_datetime(dt.datetime(2024, 1, 1, 1, 1, 1, 1, tzinfo=dt.timezone.utc)) == 'Mon, 01 Jan 2024, 01:01:01.00+UTC'


def test_format_datetime2():
    assert logbasic.format_datetime(dt.datetime(2024, 12, 31, 23, 59, 59, 999999)) == 'Tue, 31 Dec 2024, 23:59:59.99'


def test_format_timedelta():
    assert logbasic.format_timedelta(dt.timedelta(1)) == '1D0H0M0S'


def test_format_timedelta2():
    assert logbasic.format_timedelta(dt.timedelta(minutes=289589)) == '201D2H29M0S'


def test_format_timedelta3():
    assert logbasic.format_timedelta(dt.timedelta(0)) == '0D0H0M0S'


def test_format_dict1():
    assert logbasic.format_dict({'halolo': dt.datetime(2024, 1, 1)}) == "{'halolo': datetime.datetime(2024, 1, 1, 0, 0)}"
