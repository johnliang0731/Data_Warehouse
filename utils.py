import time


def is_valid_date(year="2020", month="01", day="01"):
    this_date = '{}/{}/{}'.format(month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True
