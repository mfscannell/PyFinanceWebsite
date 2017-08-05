import datetime
from django import forms
from django.core import validators

class StockSymbolEntryForm(forms.Form):
    stockSymbol = forms.CharField(label = 'Symbol')
    firstDay = forms.DateField(label = 'Start Date',
                               initial = datetime.date.today() - datetime.timedelta(days = 180))
    secondDay = forms.DateField(label = 'End Date',
                                initial = datetime.date.today())
    botCatcher = forms.CharField(required = False,
                                 widget = forms.HiddenInput,
                                 validators = [
                                     validators.MaxLengthValidator(0)
                                 ])
