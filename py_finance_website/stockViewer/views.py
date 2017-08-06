from django.shortcuts import render
from stockViewer import forms
from py_finance import YahooFinanceClient
import json

# Create your views here.
def index(request):
    stockSymbolEntryForm = forms.StockSymbolEntryForm()
    stockViewContext = {}

    if request.method == 'POST':
        stockSymbolEntryForm = forms.StockSymbolEntryForm(request.POST)

        if  stockSymbolEntryForm.is_valid():
            print('start')
            financeClient = YahooFinanceClient(stockSymbolEntryForm.cleaned_data['stockSymbol'])
            print('done financeClient')
            stockHistory = financeClient.getHistory(str(stockSymbolEntryForm.cleaned_data['firstDay']),
                                                    str(stockSymbolEntryForm.cleaned_data['secondDay']))
            print("getHistory done")
            stockViewContext['tradingDays'] = stockHistory.tradingDays
            stockViewContext['dumJson'] = json.dumps(stockHistory.tradingDays)

    stockViewContext['stockSymbolEntryForm'] = stockSymbolEntryForm
    stockViewContext['dummy'] = 23

    print('return render')
    return render(request,
                  'stockViewer/index.html',
                  context = stockViewContext)
