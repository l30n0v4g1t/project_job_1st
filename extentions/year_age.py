from datetime import datetime, date


def check_age(birthday: datetime):
    datedelta = date(datetime.now().year, datetime.now().month, datetime.now().day) - date(birthday.year, birthday.month, birthday.day)
    return int(datedelta.days / 365.25)
