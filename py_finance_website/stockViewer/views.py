from django.shortcuts import render
from stockViewer import forms
from py_finance import YahooFinanceClient

# Create your views here.
def index(request):
    stockSymbolEntryForm = forms.StockSymbolEntryForm()
    stockSymbolFormContext = {}

    if request.method == 'POST':
        stockSymbolEntryForm = forms.StockSymbolEntryForm(request.POST)

        if  stockSymbolEntryForm.is_valid():
            print('validation success')
            print(stockSymbolEntryForm.cleaned_data['stockSymbol'])
            print(str(stockSymbolEntryForm.cleaned_data['firstDay']))
            print(str(stockSymbolEntryForm.cleaned_data['secondDay']))

            financeClient = YahooFinanceClient(stockSymbolEntryForm.cleaned_data['stockSymbol'])
            stockHistory = financeClient.getHistory(str(stockSymbolEntryForm.cleaned_data['firstDay']),
                                                    str(stockSymbolEntryForm.cleaned_data['secondDay']))
            stockSymbolFormContext['stockHistory'] = stockHistory

    stockSymbolFormContext['stockSymbolEntryForm'] = stockSymbolEntryForm

    return render(request,
                  'stockViewer/index.html',
                  context = stockSymbolFormContext)
