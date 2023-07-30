from django import template 
import datetime
register = template.Library()

@register.filter
def get_age_from_date(value):
    diff = datetime.datetime.today() - datetime.datetime.strptime(value, '%d.%m.%Y')
    diff = int(diff.days / 365)
    return diff