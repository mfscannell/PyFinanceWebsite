from django import template

register = template.Library()

@register.filter(name='getLastTradingDayHigh')
def getLastTradingDayHigh(value):
    return value.getLastTradingDay()['High']
