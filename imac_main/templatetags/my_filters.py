from datetime import datetime, timedelta
from django import template

register = template.Library()

class serialno():
    def __init__(self):
        self.sno = 0


s = serialno()


@register.filter
def is_date_greater_than_one_day(value):
    value_date = datetime.strptime(value, '%Y-%m-%d')
    one_day_later = datetime.now() + timedelta(days=1)
    return value_date > one_day_later

@register.filter
def inc(value):
    s.sno += 1
    return s.sno

@register.filter
def reset(value):
    s.sno = 0
    return s.sno