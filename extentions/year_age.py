from datetime import datetime, timedelta, tzinfo

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()


def check_age(birthday: datetime):
    time_now = datetime.now(utc) - birthday
    seconds_in_year = 365.25*24*60*60
    return int(time_now.total_seconds() / seconds_in_year)