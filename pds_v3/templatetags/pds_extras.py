from django import template
register = template.Library()
import datetime, re
from django.template.defaultfilters import stringfilter

def add_day(value):
    date = datetime.datetime.fromtimestamp(int(value))
    try:
        date = datetime.datetime(date.year,date.month, date.day+1)
    except:
        try:
            date = datetime.datetime(date.year,date.month+1, 1)
        except:
            date = datetime.datetime(date.year+1,1,1)
    return date.strftime("%B %d, %Y")

def remove_time(dt):
    return dt.strftime("%B %d, %Y")
def show_cents(value):
    return "%.2f" % float(value)
def unixtimeconvert(value):
    return datetime.datetime.fromtimestamp(int(value)).strftime("%B %d, %Y")

def multiply(value, arg):
    return int(value) * int(arg)

def fix_price(value):
    return int( float(value) * 100)

def format_cents(value):
    return float(value/100.00)

def days_since_join(value):
    now = datetime.datetime.now()
    date_joined = value
    return date_joined.days()

#[display_text](url)
@stringfilter
def add_links_to_bio(value):
    return re.sub(r"\[([\w :/.$\-_.+!*'(),]*)\]\(([\w:/.$\-_.+!*',]*)\)", r'<a target="_blank" href="\2">\1</a>', value)

@stringfilter
def no_links(value):
    return re.sub(r"\[([\w :/.$\-_.+!*'(),]*)\]\(([\w:/.$\-_.+!*',]*)\)", r'\1', value)

def cutlel(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

register.filter('no_links', no_links)
register.filter('add_links_to_bio', add_links_to_bio)
register.filter('remove_time', remove_time)
register.filter('show_cents', show_cents)
register.filter('unix_time_convert', unixtimeconvert)
register.filter('add_day', add_day)
register.filter('days_since_join', days_since_join)
register.filter('fix_price', fix_price)
register.filter('format_cents', format_cents)
