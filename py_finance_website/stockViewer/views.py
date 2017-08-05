from django.shortcuts import render
from stockViewer import forms
from py_finance import YahooFinanceClient

# Create your views here.
def index(request):
    stockSymbolEntryForm = forms.StockSymbolEntryForm()
    stockViewContext = {}

    if request.method == 'POST':
        stockSymbolEntryForm = forms.StockSymbolEntryForm(request.POST)

        if  stockSymbolEntryForm.is_valid():
            financeClient = YahooFinanceClient(stockSymbolEntryForm.cleaned_data['stockSymbol'])
            stockHistory = financeClient.getHistory(str(stockSymbolEntryForm.cleaned_data['firstDay']),
                                                    str(stockSymbolEntryForm.cleaned_data['secondDay']))
            print("getHistory done")
            stockViewContext['tradingDays'] = stockHistory.tradingDays

    stockViewContext['stockSymbolEntryForm'] = stockSymbolEntryForm

    print('return render')
    return render(request,
                  'stockViewer/index.html',
                  context = stockViewContext)
